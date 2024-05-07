from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pytube import YouTube
from transformers import pipeline
from assemblyai import Transcriber, TranscriptionConfig
from django.conf import settings
import os

def index(request):
    if request.method == 'POST':
        video_url = request.POST.get('youtube_url')

        try:
            yt = YouTube(video_url)
            video_title = yt.title

            context = {'video_title': video_title}
            return render(request, 'generic.html', context)
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')

    return render(request, 'index.html')

def generic(request):
    if request.method == 'POST':
        video_url = request.POST.get('youtube_url')
        keywords = request.POST.get('keywords', '')  # Extract keywords from form data

        # Check if the URL is a valid YouTube link
        if 'youtube.com' not in video_url and 'youtu.be' not in video_url:
            return render(request, 'index.html', {'invalid_link': True})

        # Load the YouTube video
        try:
            yt = YouTube(video_url)
            video_title = yt.title

            # Filter audio streams for English language
            english_audio_streams = [s for s in yt.streams.filter(only_audio=True) if s.abr.startswith('160k')]

            # Choose the first available English audio stream, or default to the first available audio stream
            audio_stream = english_audio_streams[0] if english_audio_streams else yt.streams.filter(only_audio=True).first()

            # Use video title as the audio file name
            audio_filename = f"{video_title}.mp4"
            audio_path = os.path.join(settings.BASE_DIR, 'media', audio_filename)

            # Download the audio stream
            if not os.path.exists(audio_path):
                audio_stream.download(output_path=os.path.join(settings.BASE_DIR, 'media'), filename=audio_filename)

            # Transcribe the audio in English
            transcriber = Transcriber()
            config = TranscriptionConfig(language_code="en")
            transcript = transcriber.transcribe(audio_path, config=config)

            if not transcript or not transcript.text:
                return HttpResponse("Transcription failed. Please try again with a different video.")

            # Extract text from the Transcript object
            transcript_text = transcript.text

            # Combine transcript text with keywords
            text_with_keywords = f"{transcript_text} {keywords}"

            # Split text into smaller chunks
            chunk_size = 600  # Adjust this value as needed
            chunks = [text_with_keywords[i:i+chunk_size] for i in range(0, len(text_with_keywords), chunk_size)]

            # Initialize the summarizer for English
            summarizer_en = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

            summary_texts = []
            for chunk in chunks:
                try:
                    # Summarize the chunk
                    summary_text = summarizer_en(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
                    summary_texts.append(summary_text)
                except Exception as e:
                    return HttpResponse(f'Error summarizing: {str(e)}')

            return render(request, 'generic.html', {'video_title': video_title, 'summarized_texts': summary_texts})

        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')

    return render(request, 'generic.html')

def generate_pdf(request):
    if request.method == 'POST':
        # Get the summarized texts from the form data
        summarized_texts = request.POST.getlist('summary_text')

        if not summarized_texts:
            return HttpResponse("No summarized texts provided")

        # Create a PDF file
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="summary.pdf"'

        # Create a canvas object
        p = canvas.Canvas(response, pagesize=letter)

        # Set up the coordinates for text rendering
        y_position = 750  # Starting y position for text

        # Add each summarized text to the PDF
        for text in summarized_texts:
            p.drawString(100, y_position, text)
            y_position -= 20  # Adjust this value for spacing between texts

        # Save the PDF
        p.showPage()
        p.save()

        return response
    elif request.method == 'GET':
        # Handling GET requests
        return HttpResponseNotAllowed(['POST'])

def invalid_link(request):
    return render(request, 'invalid_link.html')
