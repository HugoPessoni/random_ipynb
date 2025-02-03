import openai
import os
import time
from dotenv import load_dotenv

load_dotenv()

openai.api_key  = os.getenv('OPENAI_API_KEY')

# Função da requisição para o modelo da OpenAI
def get_completion(prompt, model="gpt-3.5-turbo"): 
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

tema = """Impactos do garimpo ilegal no meio ambiente e na economia"""
texto = """
    Discute-se muito sobre os impactos do garimpo ilegal no meio \
    ambiente e na economia, devido a sua relevância na sociedade \
    brasileira e organizações ambientais. há que se considerar os \
    efeitos deste problema na vida das pessoas envolvidas e saná-lo. \
    Os problemas são degradação ambiental, prejuízos sociais e o não \
    avanço social a econômico, e uma solução possível seria o reforço \
    das leis e a fiscalização ambiental. Observa-se que tal cenário é \
    maléfico ao meio ambiente, pois causa grandes problemas como erosão, \
    desmatamento e destruição em habitats naturais, além de prejudicar \
    animais e rios, expulsando a caça e a pesca da qual os povos e \
    comunidades se alimentam, causando então, danos inseparaveis a \
    natureza. A floresta amazônica por exemplo garante chuvas para \
    boa parte da América do Sul e tem grande contribuição no combate \
    ao aquecimento global e às mudanças climáticas. Tem uma imensa \
    diversidade biologica, com milhares de espécies de plantas e \
    animais, é berço da maior bacia hidrográfica do mundo, por isso \
    é muito importante a sua proservação, os efeitos da garimpagem \
    não são capazes de resolver mudanças significativas nesses \
    locais, mantendo a natureza em desgaste e população onde \
    ocorre na pobreza. Além dessa realidade de desrespeito para \
    com o meio ambiente e comunidades, outro grande problema dessa \
    crise é o não avanço econômico social. Causando assim a pobreza, \
    doenças, falta de educação e o não acesso aos direitos como \
    mostra no IPS (Índice de Progreso Social), o número de localidades \
    afetadas pelo garimpo possuem um indicador de IPS de 52,4, \
    número menor que a média amazônica e brasileira. Em virtude dos \
    fatos mencionados para resolver esses problemas n desenvolvimento \
    e na natureza, cabe ao Ministério de Justiça e Segurança Pública, \
    órgão que garante os direitos públicos e segurança pública, \
    promover com o auxílio do Ibama (Instituto Brasileiro do \
    Meio Ambiente e dos Recursos Naturais Renováveis) o controle \
    e fiscalização dessas comunidades, pois é imperativo garantir \
    o controle e prevenção de possíveis problemas ambientais, \
    Ademais, cabe ao Ministério de Minas e Energia, com o ANM \
    (Agência Nacional de Mineração) órgão com a função de \
    fiscalizar, e em lei de criar regras para a preservação do \
    meio ambiente, resolver o problema do garimpo ilegal, \
    reforçando ainda mais leis que de o fim e seja barrado o avanço \
    dessa prática no ambiente. Assim a dignidade dos povos \
    originários do brasil seria respeitada assim como resolveria \
    problemas no clima global e na economia.
"""

# Prompt de instrução de correção para o modelo
prompt = f"""
    Sua tarefa é avaliar a seguinte redação entre crases triplas \
    como se fosse um corretor da prova de redação do ENEM. \
    Faça a avaliação com base nos critérios de adotados pelo ENEM. \
    Considere os níveis de desempenho pra cada \
    competência (Nível 0 a Nível 5). Os critérios \
    de avaliação do ENEM são:
    1 - Domínio da escrita formal em língua portuguesa. \
    Se o texto tiver uma linguagem informal, zere a nota do critério 1;
    2 - Compreensão do tema e aplicação das áreas de conhecimento;
    3 - Capacidade de interpretação das informações e organização \
    dos argumentos;
    4 - Domínio dos mecanismos linguísticos de argumentação;
    5 - Capacidade de conclusão com propostas coerentes que respeitem \
    os direitos humanos.

    Analise cada tópico das competências de avaliação individualmente \
    em relação ao texto para chegar na conclusão da avaliação.

    Para as seguintes características do texto, a nota da avaliação \
    deve ser 0 para todas as competências de avaliação.

    1 - Texto fora do tema proposto (ZERAR TODAS AS COMPETÊNCIAS); 
    2 - Não obediência ao tipo dissertativo-argumentativo \
    (ZERAR TODAS AS COMPETÊNCIAS);
    3 - Números ou sinais gráficos sem função evidente em \
    qualquer parte do texto;
    4 - Parte deliberadamente desconectada do tema proposto \
    (ZERAR TODAS AS COMPETÊNCIAS);
    5 - Impropérios e outros termos ofensivos, ainda que façam \
    parte do projeto de texto (ZERAR TODAS AS COMPETÊNCIAS);
    6 - Aceitar apenas Português do Brasil (Caso seja outra língua \
    também deve zerar todas as competências);
    7 - Não seguir a escrita formal em língua portuguesa \
    (ZERAR TODAS AS COMPETÊNCIAS).

    Siga sempre com muito rigor todos os critérios passados \
    para a avaliação e os critérios para zerar a nota das competências.
    Dessa forma seguem os dados:
    Tema: {tema}
    Texto: ```{texto}```

    Forneça a resposta no seguinte formato JSON:
    {{
        "competencia_1_nivel": {{nível}},
        "competencia_2_nivel": {{nível}},
        "competencia_3_nivel": {{nível}},
        "competencia_4_nivel": {{nível}},
        "competencia_5_nivel": {{nível}},
        "comentario": {{comentario}}
    }}
"""
# Guarda o horário antes da requisição ser enviada
start_time = time.time()
# Envia a requisição e guarda em 'response'
response = get_completion(prompt)
# Guarda o horário após a requisição ser finalizada
end_time = time.time()
# Calcula o tempo gasto para a requisição retornar
elapsed_time = end_time - start_time

# Etrega a resposta e o tempo gasto para finalizar
print(response)
print(elapsed_time)
