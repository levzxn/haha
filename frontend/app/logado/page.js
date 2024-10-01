'use client'
import { useRouter } from "next/navigation";
import Cookies from "js-cookie";
import { useEffect, useState } from "react";

export default function logado() {
    const [dadosUsuario, setDadosUsuario] = useState()
    const token = Cookies.get('auth-token')
    const router = useRouter()

    useEffect(() => {
        async function fetchDados() {
            if (token) {
                const dados = await getDados(token)
                setDadosUsuario(dados)
            } else {
                router.push('/')
            }
        }
        fetchDados()
    }, [])

    async function getDados(token) {
        const conexao = await fetch('http://127.0.0.1:8000/user/me',
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            }
        )
        try {
            const dados = await conexao.json()
            return dados
        }
        catch (error) {
            return error
        }
    }
    function deslogar() {
        Cookies.remove('auth-token')
        router.push('/')
    }
    function irParaUpload(){
        router.push('/logado/upload')
    }
    return (
        <div>
            {dadosUsuario ?
                <div>
                    <h1>Seu nome: {dadosUsuario.username}</h1>
                    <h2>Seu email: {dadosUsuario.email}</h2>
                    <button onClick={deslogar}>Deslogar</button>
                </div>
             :
             <p>Carregando dados do usuário...</p>
            }
            <button onClick={irParaUpload}>ir para Upload</button>
        </div>
    );
}