'use client'
export default function Upload() {
    async function enviarArquivo(evento) {
        evento.preventDefault()
        const dadosFormulario = new FormData(evento.target)
        console.log(dadosFormulario)
        const conexao = await fetch('http://localhost:8000/docs/uploadfile', {
            method: 'POST',
            body: dadosFormulario 
        })
        try {
            const dados = await conexao.json()
            console.log(dados)
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