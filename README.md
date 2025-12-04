# Cyber Jumper

**Cyber Jumper** é um jogo de plataforma 2D desenvolvido em Python utilizando a biblioteca **PgZero**. O projeto foi criado como parte de um teste de proficiência técnica, demonstrando o uso de lógica de programação, orientação a objetos e manipulação de sprites sem depender de frameworks complexos de terceiros (além do permitido).

## 📋 Sobre o Projeto

Eu desenvolvi esse jogo respeitando rigorosamente os requisitos técnicos definidos:
* **Gênero:** Platformer (visão lateral com gravidade e pulo).
* **Bibliotecas:** Uso restrito a `pgzero`, `math` e `random`.
* **Estrutura:** Código limpo (PEP8), uso de Classes para Entidades, Jogador e Inimigos.
* **Funcionalidades:**
    * Menu Principal interativo (Iniciar, Som On/Off, Sair).
    * Animação de Sprites (Idle e Walk) para todos os personagens.
    * Sistema de colisão e física (gravidade).
    * Múltiplos níveis e luta contra Chefe (Boss).

## 🎮 Como Jogar

O objetivo é bem simples: atravesse as plataformas, derrotar os inimigos e vençer o Boss final.

* **Mecânica de Combate:** Assim como nos clássicos jogos de plataforma, para derrotar um inimigo ou o Boss, você deve **pular na cabeça deles** enquanto estiver caindo.
* **Vidas:** O jogador começa com 3 vidas.

### Controles

| Tecla | Ação |
| :--- | :--- |
| **Seta Esquerda** | Mover para a Esquerda |
| **Seta Direita** | Mover para a Direita |
| **Seta Cima** | Pular |
| **Espaço** | Voltar ao Menu (na tela de Vitória/Derrota) |
| **Mouse** | Interagir com o Menu Principal |

## 🛠️ Instalação e Execução

Siga os passos abaixo para configurar o ambiente e rodar o jogo.

### Pré-requisitos
* Python 3.x instalado.

### 1. Instalar Dependências
O projeto possui um arquivo `requirements.txt` listando as bibliotecas necessárias (`pgzero` e `pygame`). Execute o seguinte comando no seu terminal:

```
pip install -r requirements.txt
```

### 2. Rodar o jogo
Para iniciar o jogo, utilize o comando abaixo. O parâmetro ```-m pgzrun``` é necessário para inicializar o contexto do Pygame Zero corretamente:

```
python -m pgzrun main.py
```

## Estrutura do Código
O projeto é contido em um arquivo principal (```main.py```) e pastas de recursos, seguindo a arquitetura que foi exigida:

- ```AnimatedEntity```: Classe base que vai fazer o gerencimento da lógica da animação de sprites (a troca ciclica de imagens, para dar um ar mais refinado ao jogo);

- ```Player```: Controla a física, o input do usuário e a gravidade;

- ```Enemy```: IA simples de patrulha;

- ```Boss```: IA de combate com projéteis (adorei codar isso haha);

- ```Button```: Classe unitária para os botões no menu;

OBS.: O jogo requer que as pastas imagens/ e sounds/ estejam no mesmo diretório do sctipt principal, para que sejam carregadas as imagens e os sons.

Desenvolvido em Python com PgZero.