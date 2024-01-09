from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import fitz
import tempfile


class ParsePDFView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        # Check if the 'file' is present in request.FILES
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=400)

        pdf_file = request.FILES['file']

        # Automatically convert the input into a list
        user_keywords = request.data.get('keyword', [])

        try:
            # Create a temporary file to store the uploaded content
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in pdf_file.chunks():
                    temp_file.write(chunk)

                temp_file_path = temp_file.name

                text_content = []

                with fitz.open(temp_file_path) as pdf_document:
                    num_pages = pdf_document.page_count

                    # Extract text content from each page
                    for page_num in range(num_pages):
                        page = pdf_document[page_num]
                        page_text = page.get_text()
                        text_content.append(page_text)

                # Convert the array of text content into a single string of words
                all_text = ' '.join(text_content)

                # Check for keyword matches
                keyword_matches = []
                string_keyword_user = ''.join(user_keywords)
                all_words = all_text.lower().split()

                if string_keyword_user in all_words:
                    keyword_matches.append(user_keywords)

                string_keywords = ''.join(keyword_matches)

                # Calculate matching percentage
                matching_percentage = (len(string_keywords) / len(user_keywords)) * 100

                return Response({
                    'num_pages': num_pages,
                    'text_content': text_content,
                    'matching_keywords': list(keyword_matches),
                    'matching_percentage': matching_percentage
                })

        except Exception as e:
            return Response({'error': str(e)}, status=500)
