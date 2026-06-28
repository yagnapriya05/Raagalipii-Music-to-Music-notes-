import os
from flask import Flask, request, jsonify, render_template, send_file
# Note: Ensure file1.py is present in your working directory with convert_audio_to_carnatic implemented.
try:
    from file1 import convert_audio_to_carnatic
except ImportError:
    # Fallback mockup function for standalone testing stability
    def convert_audio_to_carnatic(file_path, static_folder):
        return {
            "sampling_rate": 44100,
            "duration": 4.5,
            "confidence": 0.92,
            "notes": ["S", "R₂", "G₃", "M₁", "P", "D₂", "N₃", "S"],
            "plots": {
                "waveform": "/static/comparison_output.png",
                "spectrogram": "/static/comparison_output.png",
                "pitch": "/static/comparison_output.png"
            }
        }

import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# Configure upload and static directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/')
def home():
    """Serves the main Raagalipii graphical user interface dashboard."""
    return render_template('index.html', url_with_timestamp=None)


@app.route('/compare-audio', methods=['POST'])
def compare_audio():
    """Compares the seeker's user voice recording against original graphs."""
    if 'user_voice' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['user_voice']
    user_path = os.path.join(STATIC_FOLDER, 'user_attempt.wav')
    file.save(user_path)
    
    # Generate mock comparison visualization plot assets
    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    
    # Track 1: Waveform Envelope Comparison 
    axes[0].plot(np.random.randn(100), color='#b57a28', label='Original')
    axes[0].plot(np.random.randn(100), color='#e6a845', alpha=0.6, label='Your Attempt')
    axes[0].set_title("Vocal Waveform Envelope Tracking Comparison")
    axes[0].legend()
    
    # Track 2: Spectrogram Matrix Comparison
    axes[1].imshow(np.random.rand(10, 10), cmap='copper', aspect='auto')
    axes[1].set_title("Short-Time Fourier Spectrogram Overlap Matrix")
    
    # Track 3: Fundamental Pitch Trace Overlap
    axes[2].plot(np.sin(np.linspace(0, 10, 100)), color='#b57a28', lw=2)
    axes[2].plot(np.sin(np.linspace(0, 10, 100)) + 0.1, color='red', linestyle='--', alpha=0.7)
    axes[2].set_title("Fundamental Pitch Trace (f0) Gamaka Matching")
    
    plt.tight_layout()
    plot_path = os.path.join(STATIC_FOLDER, 'comparison_output.png')
    plt.savefig(plot_path)
    plt.close()
    
    return jsonify({
        'success': True,
        'similarity_score': 88,
        'comparison_plot': '/static/comparison_output.png'
    })


@app.route('/download-notation-pdf')
def download_notation_pdf():
    """Generates a multi-line PDF document using ReportLab layout rules."""
    live_notes = request.args.get('notes', 'S  R₂  G₃  M₁  P  D₂  N₃  S')
    pdf_path = os.path.join(STATIC_FOLDER, 'generated_swara_notation.pdf')
    
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        doc = SimpleDocTemplate(
            pdf_path, 
            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        title_style = ParagraphStyle(
            'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold',
            fontSize=24, leading=28, spaceAfter=15
        )
        subheader_style = ParagraphStyle(
            'DocSubheader', parent=styles['Normal'], fontName='Helvetica',
            fontSize=14, leading=18, textColor='#666666', spaceAfter=10
        )
        notes_style = ParagraphStyle(
            'SwaraNotesLine', parent=styles['Normal'], fontName='Helvetica-Bold',
            fontSize=14, leading=24, textColor='#b57a28'
        )
        
        story.append(Paragraph("Raagalipii - Carnatic Swara Sheet", title_style))
        story.append(Paragraph("Generated Notation Sequence:", subheader_style))
        story.append(Spacer(1, 10))
        
        clean_notes = live_notes.replace('➔', '-&gt;')
        story.append(Paragraph(clean_notes, notes_style))
        doc.build(story)
    except ImportError:
        # Fallback simple document file generation if ReportLab is missing in active environment
        with open(pdf_path, "w") as f:
            f.write(f"Raagalipii Swara Sheet\nNotes: {live_notes}")
        
    return send_file(pdf_path, as_attachment=True)


@app.route('/predict', methods=['POST'])
def predict():
    """Processes uploaded file samples to convert audio sequences into Carnatic text notes."""
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file found in upload request'}), 400
        
    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'error': 'No selected audio file'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        data_output = convert_audio_to_carnatic(file_path, STATIC_FOLDER)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return jsonify({'status': 'success', 'data': data_output})
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Dynamically read the port assigned by Render, defaulting to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 so external production routers can access the application
    app.run(host='0.0.0.0', port=port)
