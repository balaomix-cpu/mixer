import streamlit as st
from pydub import AudioSegment
import io
import os

# Configuração da página
st.set_page_config(page_title="Mixador de Áudio Pro", page_icon="🎙️")

st.title("🎙️ Mixador de Podcast Automático")
st.markdown("""
Este app automatiza sua edição:
1. Adiciona a **Vinheta de Entrada**.
2. Inicia a **Trilha de Fundo**.
3. Após **1 segundo**, entra sua **Gravação**.
4. Após o fim da fala, a trilha segue por **1 segundo** e faz um fade-out.
5. Finaliza com a **Vinheta de Saída**.
""")

# Upload do áudio enviado pelo celular
arquivo_voz = st.file_uploader("Envie seu áudio (.m4a, .mp3 ou .wav)", type=["m4a", "mp3", "wav"])

if arquivo_voz:
    st.audio(arquivo_voz, format='audio/m4a')
    
    if st.button("✨ Gerar Áudio Mixado Profissional"):
        with st.spinner("Processando... Aguarde a mixagem."):
            try:
                # 1. Carregar a voz enviada
                voz = AudioSegment.from_file(arquivo_voz)
                
                # Caminhos dos arquivos na pasta assets
                path_intro = "assets/intro.mp3"
                path_saida = "assets/saida.mp3"
                path_trilha = "assets/trilha_fundo.mp3"

                if not all(os.path.exists(p) for p in [path_intro, path_saida, path_trilha]):
                    st.error("Erro: Verifique se os arquivos 'intro.mp3', 'saida.mp3' e 'trilha_fundo.mp3' estão na pasta 'assets'.")
                else:
                    intro = AudioSegment.from_file(path_intro)
                    saida = AudioSegment.from_file(path_saida)
                    trilha = AudioSegment.from_file(path_trilha)

                    # --- LÓGICA DE MIXAGEM PROFISSIONAL ---
                    respiro = 1000  # 1 segundo em milissegundos
                    
                    # Ajustar volume da trilha (BG) -25dB para não abafar a voz
                    bg = trilha - 25 
                    
                    # Duração total necessária para a trilha: 1s + Voz + 1s
                    duracao_total_meio = respiro + len(voz) + respiro
                    
                    # Garantir que a trilha cubra todo o tempo (loop se necessário e corte exato)
                    bg_ajustado = (bg * (duracao_total_meio // len(bg) + 1))[:duracao_total_meio]
                    
                    # Aplicar um leve fade out na trilha no último segundo para suavizar
                    bg_ajustado = bg_ajustado.fade_out(1000)

                    # A MÁGICA: Sobrepor a voz na trilha com o atraso de 1 segundo
                    # A trilha (bg_ajustado) é a base. A voz é o overlay.
                    meio_mixado = bg_ajustado.overlay(voz, position=respiro)
                    
                    # União final das partes
                    audio_final = intro + meio_mixado + saida
                    # ---------------------------------------

                    # Exportar para o buffer de memória
                    buffer = io.BytesIO()
                    audio_final.export(buffer, format="mp3")
                    
                    st.success("✅ Áudio mixado com sucesso!")
                    st.audio(buffer, format="audio/mp3")
                    
                    st.download_button(
                        label="📥 Baixar Áudio Final",
                        data=buffer.getvalue(),
                        file_name="audio_final_mixado.mp3",
                        mime="audio/mp3"
                    )
                    
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")
                st.info("Dica: Verifique se a versão do Python no Streamlit Cloud está em 3.11 ou 3.12.")

st.caption("Ferramenta de edição automatizada.")
