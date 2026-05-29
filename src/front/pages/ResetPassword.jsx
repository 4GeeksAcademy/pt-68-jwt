import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export const ResetPassword = () => {
    const [email, setEmail] = useState("");
    const [code, setCode] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const backendUrl = import.meta.env.VITE_BACKEND_URL;
            const response = await fetch(`${backendUrl}/api/reset-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, code, password })
            });

            const data = await response.json();
            setMessage(data.message);

            if (response.ok) {
                setTimeout(() => navigate("/login"), 3000);
            }
        } catch (error) {
            setMessage("Error al procesar la solicitud.");
        }
    };

    return (
        <div className="container mt-5">
            <h2>Restablecer Contraseña</h2>
            <form onSubmit={handleSubmit}>
                <input type="email" placeholder="Tu email" className="form-control mb-2" onChange={(e) => setEmail(e.target.value)} required />
                <input type="text" placeholder="Código de 6 dígitos" className="form-control mb-2" onChange={(e) => setCode(e.target.value)} required />
                <input type="password" placeholder="Nueva contraseña" className="form-control mb-2" onChange={(e) => setPassword(e.target.value)} required />
                <button type="submit" className="btn btn-success">Actualizar Contraseña</button>
            </form>
            {message && <div className="alert alert-info mt-3">{message}</div>}
        </div>
    );
};