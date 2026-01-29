from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated          
from rest_framework.authentication import TokenAuthentication 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import pandas as pd
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Dataset


@method_decorator(csrf_exempt, name='dispatch')
class UploadCSV(APIView):
    authentication_classes = [TokenAuthentication]      
    permission_classes = [IsAuthenticated]              
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES['file']
        df = pd.read_csv(file)
        
        required_cols = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        if not all(col in df.columns for col in required_cols):
            return Response({'error': f'Missing columns: {required_cols}'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        summary = {
            'total_count': len(df),
            'averages': df[numeric_cols].mean().to_dict(),
            'type_distribution': df['Type'].value_counts().to_dict()
        }
        
        Dataset.objects.create(
            name=file.name,
            csv_data=df.to_json(orient='records'),
            summary=summary
        )
        return Response(summary, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class SummaryList(APIView):
    authentication_classes = [TokenAuthentication]      
    permission_classes = [IsAuthenticated]             
    def get(self, request):
        datasets = Dataset.objects.all()[:5]
        return Response([{
            'id': d.id,
            'name': d.name,
            'summary': d.summary
        } for d in datasets])

@method_decorator(csrf_exempt, name='dispatch')
class GeneratePDF(APIView):
    authentication_classes = [TokenAuthentication]      
    permission_classes = [IsAuthenticated]              
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
            df = pd.read_json(dataset.csv_data, orient='records')
            
            # Create PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{dataset.name}_report.pdf"'
            p = canvas.Canvas(response, pagesize=letter)
            
            # Title
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, 750, f"Chemical Equipment Report")
            p.setFont("Helvetica", 12)
            p.drawString(100, 730, f"Dataset: {dataset.name}")
            p.drawString(100, 710, f"Total Records: {dataset.summary['total_count']}")
            
            # Averages Table
            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, 680, "AVERAGES:")
            y = 660
            p.setFont("Helvetica", 12)
            for param, avg in dataset.summary['averages'].items():
                p.drawString(120, y, f"{param}: {avg:.2f}")
                y -= 20
            
            # Type Distribution
            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, y-10, "TYPE DISTRIBUTION:")
            y -= 30
            p.setFont("Helvetica", 12)
            for equipment_type, count in list(dataset.summary['type_distribution'].items())[:5]:
                p.drawString(120, y, f"{equipment_type}: {count}")
                y -= 20
                
            p.showPage()
            p.save()
            return response
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=404)
