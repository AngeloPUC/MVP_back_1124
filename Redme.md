
## Como executar a API
Para rodar a API, você precisa garantir que todas as dependências estão instaladas e que o ambiente está configurado corretamente.

Antes de tudo:
Abra o Windows Power Shell
use o comando: cd "/caminho para o seu/projeto"

# 1 passo: Clonar o repositorio (ambiente virtual)
É necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.
É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Na diretorio use:
crei o ambiente virtual: python -m venv venv
ative o ambiente virtual: venv\Scripts\activate
caso queira desativar o ambiente virtual usar: deactivate (apenas desativa sem eliminar a pasta)

# 2 passo: Instalar as bibliotcas do requirements
Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
comando: pip install -r requirements.txt

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

# 3 passo: Executar a API
Para executar a API  basta executar:
comando: flask run --host 0.0.0.0 --port 5000

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

comando: flask run --host 0.0.0.0 --port 5000 --reload

# 4 passo: consulta

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
