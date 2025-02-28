import { useState } from "react";
import { Camera } from "react-camera-pro";
import axios from "axios";
import { Button, Card, CardContent, Input } from "@/components/ui";

export default function QRScanner() {
    const [qrImage, setQrImage] = useState(null);
    const [camera, setCamera] = useState(null);
    const [result, setResult] = useState(null);

    const handleCapture = () => {
        if (camera) {
            const image = camera.takePhoto();
            setQrImage(image);
        }
    };

    const handleUpload = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => setQrImage(reader.result);
            reader.readAsDataURL(file);
        }
    };

    const validateQR = async () => {
        try {
            const formData = new FormData();
            formData.append("file", qrImage);
            const response = await axios.post("https://tu-backend.com/validate_qr", formData);
            setResult(response.data.message);
        } catch (error) {
            setResult("QR no válido");
        }
    };

    return (
        <div className="flex flex-col items-center gap-4 p-6">
            <Card className="w-full max-w-md">
                <CardContent className="flex flex-col items-center gap-4">
                    <Camera ref={setCamera} className="w-full h-60 border rounded-xl" />
                    <Button onClick={handleCapture}>Capturar QR</Button>
                    <Input type="file" accept="image/*" onChange={handleUpload} />
                    {qrImage && <img src={qrImage} alt="QR Preview" className="w-40 h-40 border" />}
                    <Button onClick={validateQR} disabled={!qrImage}>Validar QR</Button>
                    {result && <p className="text-lg font-bold">{result}</p>}
                </CardContent>
            </Card>
        </div>
    );
}
