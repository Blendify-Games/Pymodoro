# Pymodoro 🍅 (see in [🇺🇸](./README-en_US.md))

Uma implementação simples de pomodoro usando [pygame-ce](https://github.com/pygame-community/pygame-ce) e estética retrogame. Esta aplicação tem a função de te deixar feliz e também controlar seu tempo enquanto você trabalha. 😊

Veja esta [seção](#como-rodar-o-pymodoro-no-meu-computador) para entender como rodar esta aplicação.

O Pymodoro é conceituralmente simples, você ajusta dois ou quatro parâmetros e depois você aperta o botão de play. Os parâmetros são "Trabalho", "Descanso", "Ciclos antes do descanso longo" e "Tempo de descanso longo".

| Parâmetro | Descrição | Valor Padrão |
|-----------|-----------|--------------|
| Trabalho | O tempo que você deseja gastar trabalhando em minutos | 25 minutos |
| Descanso | O tempo que você deseja gastar descansando em minutos antes de recomeçar o ciclo de trabalho | 5 minutos |
| Ciclos antes do descanso longo | Número de ciclos de (trabalho + descanso) antes de ter um descanso longo. Se zero, não haverá descanso longo | 0 minutos (desabilitado) |
| Tempo de descanso longo | O tempo que você irá gastar a cada descanso longo em minutos. Se zero, não haverá descanso longo | 0 minutos (desabilitado) |

## Usando o Pymodoro

### A cena de ajustes

Considere ler o que o Pymodoro 🍅 tem a dizer a você, ele irá explicar como ajustar e usar a aplicação:

<img src=screenshots/setup-pt_BR.png>

### A cena de visualização

Nesta cena você irá ver um temporizador com a descrição do ciclo. O botão de informação lhe dará as estatísticas de uso do Pymodoro. O botão verde (⬅️) lhe possibilitará a voltar para a cena de ajustes do Pymodoro. Lembre-se de que, ao voltar, o progresso feito até agora no pomodoro vigente será perdido.

<img src=screenshots/show-pt_BR.png>

## Como rodar o Pymodoro no meu computador?

Você pode escolher duas formas de executar o Pymodoro. Uma forma é [baixando o *release*](#baixando-um-release-executável) que constitui uma forma rápida e fácil, entretanto, pode não existir uma versão adequada para o seu sistema operacional. A outra forma é [baixando o repositório](#baixando-o-repositório) que pode necessitar um pouco mais de experiência com a ambientação da linguagem de programação Python.

### Baixando um *release* executável

No repositório do [Github](https://github.com/Blendify-Games/Pymodoro) vá no canto direito e busque pelo link `Pomodoro v1.0.1`. Escolha a versão do *release* que deseja, se para **Windows** ou **Linux** (ambos apenas para x86_64). Depois, basta descompatar e clicar no arquivo para executar o Pymodoro.

### Baixando o repositório
Esta aplicação foi desenvolvida utilizando python 3.12.1. Após a instalação do python, é recomendável que você crie um ambiente virtual de execução para as bibliotecas utilizadas neste projeto. Utilize o virtualenv para tal. Faça a instalação do virtualenv e, dentro da pasta do repositório Pymodoro, crie um ambiente virtual. Acesse um terminal e digite:

```bash
> pip install virtualenv     # instalação do virtualenv
> virtualenv .venv           # criação do ambiente virtual
#------ Alternativamente
> pip3 install virtualenv    # utilize pip3 quando há versões 2.* e 3.* do python
> python3 -m venv .venv      # criação do ambiente virtual
```

Após a primeira execução, para rodar o Pymodoro, repita apenas os passos 1 e 3.

1. Ative o ambiente virtual

    ```bash
    # No windows faça
    > .\.venv\Scripts\activate

    # No GNU/Linux ou outros SOs unix-like faça
    $ source ./.venv/bin/activate
    ```
    * Observe que ao entrar no ambiente virtual, algo como `(.venv)` irá aparecer no início da linha. Isto indica que o ambiente virtual está ativado. Para desativar, digite `deactivate`.

2. Caso seja a primeira execução neste ambiente virtual, instale as dependências necessárias:
    
    ```bash
    > pip install -r requirements.txt
    #------ Alternativamente
    > pip3 install -r requirements.txt      # utilize pip3 quando há versões 2.* e 3.* do python
    ```

3. Entre na pasta do `src` e execute o Pymodoro:

    ```bash
    > python main.py
    #------ Alternativamente
    > python3 main.py                       # utilize python3 quando há versões 2.* e 3.* do python
    ```
