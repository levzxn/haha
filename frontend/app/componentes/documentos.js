import Cookies from "js-cookie"
import { useEffect, useState } from "react"
import Documento from "./documento"

export default function Documentos() {
    const [listaDocumentos, setListaDocumentos] = useState([])
    const token = Cookies.get('auth-token')
    
    useEffect(() => {
        async function getDocumentos() {
            try {
                const documentosConexao = await fetch('http://localhost:8000/docs/all', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                const documentosJson = await documentosConexao.json()
                console.log(documentosJson)
                setListaDocumentos(documentosJson)
            }
            catch (error) {
                return error
            }
        }
        getDocumentos()
    }, [])

    return (
        <section>
            <h1>Lista de documentos:</h1>
            {listaDocumentos.map(documento => {
                return (
                    <Documento key={documento.id} dados={documento}></Documento>
                )
            })}
        </section>
    )
}