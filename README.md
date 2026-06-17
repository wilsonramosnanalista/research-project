# _Game Engine_ para Relização de Jogos em Documentos PDF

Este projeto permite a geração de um arquivo PDF contendo um jogo interativo executável que roda diretamente no leitor de documentos de seu navegador.

## Pré-requisitos

* Você precisa ter o _**Python**_ instalado em seu sistema operacional.
* Utilizar um dos seguintes leitores: _**Google Chrome**, **Opera**, **Brave** ou **Vivaldi**_. Os PDF interativos foram testados com sucesso nestes navegadores para os sistemas operacionais _**Windows**, **Linux**_ e _**macOS**_.

---

## Passo a Passo para Configuração de Ambiente e Utilização do Motor

### Passo 1: Instalar o _Python_ e Verificar a Configuração

1. Baixe e instale o _Python_ através do [site oficial do Python](https://www.python.org/).
   * Durante a instalação, certifique-se de marcar a caixa que diz _**"Add Python to PATH"**_ ou _**"Add python.exe to PATH"**_ antes de avançar.
2. Para verificar se a instalação foi bem-sucedida:
   * Abra o _Prompt_ de Comando (CMD) ou o _PowerShell_;
   * Execute o seguinte comando:
     ```bash
     python --version
     ```
   * Você deverá ver a versão instalada do _Python_ (ex: `Python 3.10.6`).

> 💡 *Nota: Se você encontrar um erro informando que o comando 'Python' não foi reconhecido, significa que a caixinha do "PATH" não foi marcada. Pode ser necessário reinstalar o Python marcando a opção ou adicionar o caminho manualmente nas Variáveis de Ambiente do Windows.*

### Passo 2: Baixar e Extrair o Projeto

1. Faça o download do arquivo ZIP do projeto diretamente aqui no repositório do _GitHub_;
2. Extraia o conteúdo do arquivo ZIP em uma pasta de sua preferência no seu computador.

### Passo 3: Navegar até a Pasta do Projeto

1. Abra o _Prompt_ de Comando (CMD) ou o _PowerShell_;
2. Use o comando `cd` para navegar até o diretório raiz onde você extraiu a pasta do projeto.
   * *Exemplo:*
     ```bash
     cd C:\Users\SeuUsuario\Desktop\meu-projeto
     ```

### Passo 4: Instalar as Dependências

1. Atualize o gerenciador de pacotes do _Python_ (`pip`) executando:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Instale as dependências de manipulação estrutural de PDF necessárias para o projeto (biblioteca _pdfrw_ e _reportlab_):
    ```bash
    python -m pip install pdfrw
    ```
    ```bash
    python -m pip install reportlab
    ```

### Passo 5: Abrir o Projeto no _VS Code_
1. Abra o _Visual Studio Code_ (_VS Code_);
2. No menu superior, vá em _File > Open Folder_ (Arquivo > Abrir Pasta) e selecione a pasta raiz do projeto extraída no Passo 2.

### Passo 6: Executar o _Script_ de Geração do PDF
1. Abra o Terminal Integrado no _VS Code_ indo no menu em _Terminal > New Terminal_;
2. Execute o _script_ gerador com o comando:
    ```bash    
    python main.py game_demo
    ```
3. O _script_ será executado e criará o arquivo de saída interativo chamado _game_demo.pdf_ diretamente na pasta _"\output\games"_ do seu projeto;
4. O PDF jogável abrirá automaticamente para apreciação.
   * Caso queira gerar e executar outro jogo, basta alterar o nome _"game_demo"_, conforme exemplo abaixo:
   * *Exemplo:*
     ```bash
     python main.py game_allegro
     ```
     
### Demonstração em Vídeo (_Gameplay_)
Assista ao vídeo demonstrativo da _gameplay_, que ilustra a alta interatividade e a fluidez dos jogos/animações executando diretamente dentro do documento PDF:

📺 **[Vídeo demonstrativo omitido]** 

*Nota: O link para a demonstração completa na plataforma de compartilhamento de vídeos será disponibilizado na versão final do documento, após a conclusão do processo de avaliação.*
