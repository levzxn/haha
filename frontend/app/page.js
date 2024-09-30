'use client'
import Cookies from 'js-cookie'
import { useRouter } from "next/navigation";


export default function Home() {
  const router = useRouter()

  const logar = async (evento) => {
    evento.preventDefault()
    const formData = new FormData(evento.target)
    const dados = {
      nomeUsuario: formData.get('nomeUsuario'),
      senha: formData.get('senha'),
    }
    const conexao = await fetch('http://127.0.0.1:8000/auth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: dados.nomeUsuario,
        password: dados.senha,
      })
    })

    try {
      if (conexao.status === 401) {
        throw new Error('Senha incorreta. Verifique e tente novamente.')
      } else if (conexao.status === 400) {
        throw new Error('Usuário incorreto. Verifique e tente novamente.')
      } else if (!conexao.ok) {
        throw new Error('Ocorreu um erro inesperado. Tente novamente.')
      }
      const json = await conexao.json()
      const token = json.acess_token
      Cookies.set('auth-token', token)
      router.push('/logado')
    }
    catch (error) {
      console.error(error.message)
      return error.message
    }
  }
  function handleRegistro(){
    console.log('oi')
    router.push('/registrar')
  }
  return (
    <div>
      <form onSubmit={logar}>
        <label>oi</label>
        <input placeholder="nome de usuario" required name='nomeUsuario'></input>
        <input placeholder="senha" required name='senha'></input>
        <button type="submit">login</button>
      </form>
      <label>primeiro acesso? registre-se agora</label>
      <button onClick={handleRegistro}>registrar</button>
    </div>

  );
}
