'use client'

import Documentos from "@/app/componentes/documentos"
import Cookies from "js-cookie"
import { useEffect, useState } from "react"

export default function Upload() {
    const [carregando, setCarregando] = useState(false)
    const [erroCarregamento, setErroCarregamento] = useState(null)
    const token = Cookies.get('auth-token')

    async function enviarArquivo(evento) {
        evento.preventDefault()
        setCarregando(true)
        setErroCarregamento(null)
        const dadosFormulario = new FormData(evento.target)
        try {
            const conexao = await fetch('http://localhost:8000/docs/uploadfile', {
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                method: 'POST',
                body: dadosFormulario
            })

            if (!conexao.ok) {
                throw new Error('Erro ao enviar arquivo')
            }
        } catch (error) {
            setErroCarregamento('Falha no upload do arquivo: ' + error.message)
        } finally {
            setCarregando(false)
        }
    }
    return (
        <>
            <form onSubmit={enviarArquivo}>
                <input placeholder="Título desejado do documento:" name="titulo"></input>
                <input type="file" name="file"></input>
                <button type="submit">enviar</button>
            </form>
            <div>
                {carregando && <p>Carregando arquivo...</p>}
                {!carregando && erroCarregamento && <p>{erroCarregamento}</p>}
                {!carregando && !erroCarregamento && <p>Aguardando upload do arquivo...</p>}
            </div>
            <Documentos></Documentos>
        </>
    )
}
