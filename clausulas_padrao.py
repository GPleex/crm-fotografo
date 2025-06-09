# Cláusulas padrão para contrato de ensaio
clausulas_ensaio = {
    "1ª": """Cláusula 1ª. É objetivo do presente contrato a prestação do serviço de FOTOGRAFIA a cargo do CONTRATADO para o ENSAIO FOTOGRÁFICO, a se realizar no dia {{ contrato.data_ensaio }}, aproximadamente às {{ contrato.horario_ensaio }}, em {{ contrato.cidade_estado_ensaio }}.
    """,

    "2ª": """Cláusula 2ª. O CONTRATANTE deverá comparecer ao local agendado para realização do ensaio fotográfico no horário especificado previamente, sendo permitida uma tolerância de 30 minutos antes ou depois do horário especificado previamente.
""",

    "3ª": """Cláusula 3ª. Atrasos superiores a 30 minutos do horário especificado previamente, sem aviso prévio de 1 hora antes do horário agendado, será necessário reagendar a sessão fotográfica.
""",

    "4ª": """Cláusula 4ª. O CONTRATANTE deverá efetuar o pagamento na forma e condições estabelecidas na cláusula 7ª.
""",

    "5ª": """Cláusula 5ª. O CONTRATADO entregará ao CONTRATANTE o serviço com os seguintes itens:
    {{ contrato.descricao_servico }}
""",

    "6ª": """<p>Cláusula 6ª. É dever do CONTRATADO fornecer ao CONTRATANTE, a cópia do contrato, contendo todas as especificidades da prestação de serviço contratado.</p>
""",

    "7ª": """<p>Cláusula 7ª. O presente serviço será remunerado pela quantia de {{ contrato.valor }} Referente aos serviços efetivamente prestados pelo pacote personalizado citado na cláusula5ª, cujo pagamento será efetuado da seguinte maneira:</p>
    <p>{{ contrato.forma_pagamento }}</p>
""",

    "8ª": """<p>Cláusula 8ª. Poderá o presente instrumento ser rescindido por qualquer uma das partes em caso de motivo relevante, fortuito ou força maior, não obstante a outra parte deverá ser avisada previamente no prazo de 90 (noventa) dias, antes do evento, devendo ocorrer o ressarcimento dos valores já pagos.</p>
""",

    "9ª": """<p>Cláusula 9ª. Caso o CONTRATANTE requisite a rescisão imotivada do presente contrato, os valores pagos ao CONTRATADO serão restituídos mediante pagamento de multa no valor de 20% do valor total do contrato. Em caso de rescisão imotivada pelo CONTRATADO os valores já recebidos por este deverão ser ressarcidos à CONTRATANTE. Em ambos os casos a parte que der causa à rescisão imotivada está sujeita a eventuais danos materiais e/ou morais causados.</p>
""",

    "10ª": """<p>Cláusula 10ª. O CONTRATADO assume o compromisso de realizar e entregar o serviço das fotografias em alta resolução dentro do prazo de 15 dias, a contar da data do ensaio fotográfico, de acordo com a forma estabelecida no presente contrato.</p>
""",

    "11ª": """<p>Cláusula 11ª. O CONTRATANTE autoriza o uso de imagens do evento, para divulgação em site, mostruários, portfólios e anúncios comerciais, respeitando-se a integridade e a moralidade da CONTRATANTE.</p>
    <p>Parágrafo Primeiro. Fica eleito o foro da comarca de Londrina, com exclusão de qualquer outro, por mais privilegiado que seja, para dirimir quaisquer devidas ou litígios oriundos deste contrato.</p>
""",

    "12ª": """<p>Cláusula 12ª. Os cartões de memória etc. que serão utilizados são de exclusiva propriedade do CONTRATADO, não estando incluídos no orçamento. Não serão negociados e ficarão arquivados pelo tempo determinado de um ano para cópias e/ou ampliação eventualmente solicitadas pela CONTRATANTE, a preços atualizados e combinados no momento da solicitação.</p>
""",

    "13ª": """<p>Cláusula 13ª . O CONTRATANTE tem o prazo de 5 dias a contar da data da entrega do material para solicitar qualquer alteração no material entregue, tendo um prazo de 30 dias para recebê-lo novamente. Após esse prazo, não será possível solicitar alterações.</p>
""",

    "14ª": """<p>Cláusula 14ª. O CONTRATANTE confirma estar ciente da estética, estilo artístico fotográfico e características do formato de trabalho do CONTRATADO. O CONTRATANTE não poderá exigir características externas ao trabalho feito.</p>
""",

    "15ª": """<p>Cláusula 15ª. Os arquivos originais serão armazenados por 30 dias, a contar a partir da data de entrega das fotografias digitais e/ou impressas. Os arquivos digitais entregues, serão armazenados por 1 ano, a contar a partir da data de entrega das fotografias digitais e/ou impressas.</p>
"""

}

clausulas_por_tipo = {
    "ensaio": clausulas_ensaio
#    "evento": clausulas_evento
}