'use client'

import Cookies from "js-cookie"
import { use, useEffect, useState } from "react"

export default function Upload() {
    const [dadosArquivo, setDadosArquivo] = useState(null)
    const [carregando, setCarregando] = useState(false)
    const [arquivoDecodificado, setArquivoDecodificado] = useState(false)
    const [erroCarregamento, setErroCarregamento] = useState(null)
    const [listaDocumentos, setListaDocumentos] = useState([])
    const token = Cookies.get('auth-token')

    async function enviarArquivo(evento) {
        evento.preventDefault()
        setCarregando(true) 
        setErroCarregamento(null) 

        const dadosFormulario = new FormData(evento.target)

        try {
            const conexao = await fetch('http://localhost:8000/docs/uploadfile', {
                headers:{
                    'Authorization':`Bearer ${token}`
                },
                method: 'POST',
                body: dadosFormulario
            })

            if (!conexao.ok) {
                throw new Error('Erro ao enviar arquivo')
            }

            const dados = await conexao.json()

        } catch (error) {
            setErroCarregamento('Falha no upload do arquivo: ' + error.message)
        } finally {
            setCarregando(false)
        }
    }

    useEffect(() => {
        if (dadosArquivo) {
            function decodificarArquivoBase64() {
                try {
                    const decodificado = atob(dadosArquivo)
                    const utf8String = new TextDecoder('utf-8').decode(
                        new Uint8Array([...decodificado].map(c => c.charCodeAt(0)))
                    )
                    setDadosArquivo(utf8String)
                    setArquivoDecodificado(true)
                } catch (error) {
                    setErroCarregamento('Erro na decodificação do arquivo: ' + error.message)
                }
            }
            decodificarArquivoBase64()
        
        }
    }, [dadosArquivo])

    useEffect(() =>{
        async function documentosDeUmUsuario(){
            const getDocumentos = await fetch('http://localhost:8000/docs/all',{
                headers:{
                    'Authorization':`Bearer ${token}`
                }
            })
            const documentosJson = await getDocumentos.json()
            setListaDocumentos(documentosJson)
            console.log(documentosJson)
        }
        documentosDeUmUsuario()
    },[])
    return (
        <>
            <form onSubmit={enviarArquivo}>
                <input placeholder="Título desejado do documento:" name="titulo"></input>
                <input type="file" name="file"></input>
                <button type="submit">enviar</button>
            </form>

            {carregando && <p>Carregando arquivo...</p>}
            
            {!carregando && erroCarregamento && <p>{erroCarregamento}</p>}

            {!carregando && arquivoDecodificado && <p>Arquivo decodificado com sucesso!</p>}

            {!carregando && !arquivoDecodificado && !erroCarregamento && <p>Aguardando upload do arquivo...</p>}
        </>
    )
}
