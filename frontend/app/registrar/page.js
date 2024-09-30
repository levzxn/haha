'use client'
import { useRouter } from 'next/navigation'
export default function Registrar() {
    const router = useRouter()
    async function cadastrar(evento) {
        evento.preventDefault()
        const formData = new FormData(evento.target)
        const dados = {
            nomeUsuario: formData.get('username'),
            senha: formData.get('senha'),
            email: formData.get('email')
        }
        const conexao = await fetch('http://127.0.0.1:8000/user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: dados.nomeUsuario,
                email: dados.email,
                password: dados.senha,
            })
        })
        try {
            router.push('/')
        }
        catch (error) {
            console.error(error.message)
            return error.message
        }
    }
    return (
        <form onSubmit={cadastrar}>
            <input placeholder="nome de usuário" name="username"></input>
            <input placeholder="email" name="email"></input>
            <input placeholder="senha" name="senha"></input>
            <button type="submit">registrar</button>
        </form>
    )
}