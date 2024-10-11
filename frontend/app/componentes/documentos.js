import Cookies from "js-cookie"
import { useEffect, useState } from "react"
import Documento from "./documento"

export default function ListaDocumentos(){
  const [documentosSelecionados, setDocumentosSelecionados] = useState([])
  const [listaDocumentos, setListaDocumentos] = useState([])
  const token = Cookies.get('auth-token')

  function selecionarDocumento(id) {
    setDocumentosSelecionados((selecionados) => {
      if (selecionados.includes(id)) {
        return selecionados.filter((docId) => docId !== id)
      }
      else{
        return [...selecionados, id]
      }
    })
  }

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

  const enviarDocumentos = async () => {
    let stringURL = ''
    let c = 0
    documentosSelecionados.map((documento) => {
        c++
        if (c === documentosSelecionados.length - 1){
            return(
                stringURL+=`doc_ids=${documento}&`
            )    
        }
        else{
            return(
                stringURL+=`doc_ids=${documento}`
            )
        }
    })
    const conexao = await fetch(`http://localhost:8000/docs/gerar_diario/?${stringURL}`,{method:'GET'})
    console.log(await conexao.json())
  };

  return (
    <div>
      <h2>Seus documentos</h2>
      <ul>
        {listaDocumentos && listaDocumentos.map((documento) => (
          <Documento
            key={documento.id}
            file_name={documento.file_name}
            id={documento.id}
            conteudo={documento}
            selecionado={documentosSelecionados.includes(documento.id)}
            onSelecionar={() => selecionarDocumento(documento.id)}
          />
        ))}
      </ul>
      <button onClick={enviarDocumentos}>Enviar Documentos Selecionados</button>
    </div>
  );
};
