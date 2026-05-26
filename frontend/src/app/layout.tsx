import type { Metadata } from "next";
import { Toaster } from "react-hot-toast";
import "./globals.css";

export const metadata: Metadata = {
    title: "Resource Review",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
                <Toaster position="top-right" toastOptions={{ className: "text-sm" }} />
                {children}
            </body>
        </html>
    );
}
