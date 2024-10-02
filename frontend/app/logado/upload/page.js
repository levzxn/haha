'use client'
export default function Upload() {
    async function enviarArquivo(evento) {
        evento.preventDefault()
        const dadosFormulario = new FormData(evento.target)
        const conexao = await fetch('http://localhost:8000/docs/uploadfile', {
            method: 'POST',
            body: dadosFormulario 
        })
        try {
            const dados = await conexao.json()
            const endpointDados = await fetch(`http://localhost:8000/docs/${dados.doc}/`,{
                method:'GET'
            })
            const dadosJson = await endpointDados.json()
            setDadosArquivo(dadosJson)
        } catch (error) {
            setErroCarregamento('Falha no upload do arquivo: ' + error.message)
        } finally {
            setCarregando(false)
        }
        catch(error){
            return error
        }
    }
    return (
        <form onSubmit={enviarArquivo}>
            <input placeholder="titulo desejado do documento:" name="titulo"></input>
            <input type="file" name="file"></input>
            <button>enviar</button>
        </form>
    )
}