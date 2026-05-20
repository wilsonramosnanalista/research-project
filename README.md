# Projeto de Jogos Interativos em Documentos Digitais

Este projeto permite a geração de um arquivo PDF executável contendo um jogo interativo que roda diretamente no leitor de documentos do navegador.

## Pré-requisitos

* Você precisa ter o **Python** instalado em seu sistema.
* Os arquivos PDF foram testados com sucesso nos navegadores **Google Chrome**, **Opera**, **Brave** e **Vivaldi**, para os sistemas operacionais **Windows**, **Linux** e **macOS**.

---

## Passo a Passo para Configuração e Execução

### Passo 1: Instalar o Python e Verificar a Configuração

1. Baixe e instale o Python para Windows através do [site oficial do Python](https://www.python.org/).
2. **Crucial:** Durante a instalação, certifique-se de marcar a caixa que diz **"Add Python to PATH"** ou **"Add python.exe to PATH"** antes de avançar.
3. Para verificar se a instalação foi bem-sucedida:
   * Abra o Prompt de Comando (CMD) ou o PowerShell.
   * Execute o seguinte comando:
     ```bash
     python --version
     ```
   * Você deverá ver a versão instalada do Python (ex: `Python 3.10.6`).

> 💡 *Nota: Se você encontrar um erro informando que o comando 'python' não foi reconhecido, significa que a caixinha do "PATH" não foi marcada. Pode ser necessário reinstalar o Python marcando a opção ou adicionar o caminho manualmente nas Variáveis de Ambiente do Windows.*

### Passo 2: Baixar e Extrair o Projeto

1. Faça o download do arquivo ZIP do projeto diretamente aqui no repositório do GitHub.
2. Extraia o conteúdo do arquivo ZIP em uma pasta de sua preferência no seu computador.

### Passo 3: Navegar até a Pasta do Projeto

1. Abra o Prompt de Comando (CMD) ou o PowerShell.
2. Use o comando `cd` para navegar até o diretório raiz onde você extraiu a pasta do projeto.
   * *Exemplo:*
     ```bash
     cd C:\Users\SeuUsuario\Desktop\meu-projeto
     ```

### Passo 4: Instalar as Dependências

1. Atualize o gerenciador de pacotes do Python (`pip`) executando:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Instale as dependências de manipulação estrutural de PDF necessárias para o projeto (como a biblioteca pdfrw):
    ```bash
    python -m pip install pdfrw
    ```

### Passo 5: Abrir o Projeto no VS Code
1. Abra o Visual Studio Code (VS Code).
2. No menu superior, vá em File > Open Folder... (Arquivo > Abrir Pasta) e selecione a pasta raiz do projeto extraída no Passo 2.

### Passo 6: Executar o Script de Geração
1. Abra o Terminal Integrado no VS Code pressionando Ctrl + ' ou indo no menu em Terminal > New Terminal.
2. Execute o script gerador com o comando:
    ```bash    
    python .\pdf_generator.py
    ```
3. O script será executado e criará o arquivo de saída interativo chamado game_demo.pdf diretamente na pasta do seu projeto.

### Demonstração em Vídeo (Gameplay)
Assista ao vídeo demonstrativo completo com a gameplay do jogos e animação rodando de forma fluida e em tempo real dentro do documento PDF:

📺 Game Engine para Realização de Jogos em Documentos PDF
