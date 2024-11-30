const Tesseract = require('tesseract.js');

export async function handler(req, res) {
    const { imageData } = req.body;

    try {
        const { data: { text } } = await Tesseract.recognize(imageData);
        res.status(200).json({ text });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'OCR failed' });
    }
}