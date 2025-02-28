import QRScanner from "../components/QRScanner";

export default function AdminPanel() {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
            <h1 className="text-2xl font-bold mb-4">Panel de Administración</h1>
            <QRScanner />
        </div>
    );
}