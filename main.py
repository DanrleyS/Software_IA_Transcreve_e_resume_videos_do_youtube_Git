import openai
import yt_dlp as youtube_dl
import os


openai.api_key = " " #coloca aqui a chave
if not openai.api_key:
    raise ValueError("A chave de API do OpenAI não foi encontrada no arquivo .env.")


def baixar_audio(url, filename="audio.mp3"):
    try:
        print(f"Baixando áudio do vídeo: {url}")
        ydl_opts = {
            'format': 'bestaudio/best',  # Baixa o melhor áudio disponível
            'outtmpl': filename,  # Nome do arquivo de saída
            'quiet': False,  # Para exibir mais detalhes durante o processo
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Áudio baixado com sucesso: {filename}")
    except youtube_dl.DownloadError as e:
        print(f"Erro ao baixar o áudio: {e}")
        raise

def transcrever_audio(filename):
    try:
        print("Transcrevendo áudio...")
        with open(filename, "rb") as audio_file:
            # Usando a transcrição com Whisper
            transcript = openai.Audio.transcribe(
                model="whisper-1",  # Modelo Whisper para transcrição de áudio
                file=audio_file
            )
        print("Transcrição concluída.")
        return transcript['text']  # Retorna o texto transcrito
    except openai.OpenAIError as e:
        print(f"Erro ao transcrever o áudio: {e}")
        raise

def gerar_resumo(transcript):
    try:
        print("Gerando resumo...")
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[ 
                {"role": "system", "content": "Resuma o vídeo detalhadamente em formato Markdown."},
                {"role": "user", "content": transcript}
            ]
        )
        resumo = completion['choices'][0]['message']['content']
        print("Resumo gerado com sucesso.")
        return resumo
    except openai.OpenAIError as e:
        print(f"Erro ao gerar o resumo: {e}")
        raise

def salvar_resumo(resumo, filename="resumo.md"):
    try:
        with open(filename, "w", encoding="utf-8") as md_file:
            md_file.write(resumo)
        print(f"Resumo salvo em {filename}")
    except Exception as e:
        print(f"Erro ao salvar o resumo: {e}")
        raise

def limpar_arquivos_temporarios(*filenames):
    for file in filenames:
        if os.path.exists(file):
            os.remove(file)
            print(f"Arquivo temporário removido: {file}")

def main():
    try:
        url = input("Insira a URL do vídeo do YouTube: ")
        baixar_audio(url, "audio.mp3")  # Baixa o áudio diretamente como MP3
        transcript = transcrever_audio("audio.mp3")  # Transcreve o áudio MP3
        resumo = gerar_resumo(transcript)  # Gera o resumo
        salvar_resumo(resumo)  # Salva o resumo em um arquivo
    except Exception as e:
        print(f"Erro geral: {e}")
    finally:
        limpar_arquivos_temporarios("audio.mp3")  # Limpeza do arquivo temporário

if __name__ == "__main__":
    main()
