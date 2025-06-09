# Cláusulas padrão para contrato de ensaio
clausulas_ensaio = {
    "1ª": """<p>Cláusula 1ª. É objetivo do presente contrato a prestação do serviço de FOTOGRAFIA a cargo do CONTRATADO para o ENSAIO FOTOGRÁFICO, a se realizar no dia {{ contrato.data_ensaio }}, aproximadamente às {{ contrato.horario_ensaio }}, em {{ contrato.cidade_estado_ensaio }}.</p>""",

    "2ª": """<p>Cláusula 2ª. O CONTRATANTE deverá comparecer ao local agendado para realização do ensaio fotográfico no horário especificado previamente, sendo permitida uma tolerância de 30 minutos antes ou depois do horário especificado previamente.</p>""",

    "3ª": """<p>Cláusula 3ª. Atrasos superiores a 30 minutos do horário especificado previamente, sem aviso prévio de 1 hora antes do horário agendado, será necessário reagendar a sessão fotográfica.</p>""",

    "4ª": """<p>Cláusula 4ª. O CONTRATANTE deverá efetuar o pagamento na forma e condições estabelecidas na cláusula 7ª.</p>""",

    "5ª": """<p>Cláusula 5ª. O CONTRATADO entregará ao CONTRATANTE o serviço com os seguintes itens:<br>
    {{ contrato.descricao_servico }}</p>""",

    "6ª": """<p>Cláusula 6ª. É dever do CONTRATADO fornecer ao CONTRATANTE, a cópia do contrato, contendo todas as especificidades da prestação de serviço contratado.</p>""",

    "7ª": """<p>Cláusula 7ª. O presente serviço será remunerado pela quantia de {{ contrato.valor }}, referente aos serviços efetivamente prestados pelo pacote personalizado citado na cláusula 5ª, cujo pagamento será efetuado da seguinte maneira:</p>
<p>{{ contrato.forma_pagamento }}</p>""",

    "8ª": """<p>Cláusula 8ª. Poderá o presente instrumento ser rescindido por qualquer uma das partes em caso de motivo relevante, fortuito ou força maior, não obstante a outra parte deverá ser avisada previamente no prazo de 90 (noventa) dias, antes do evento, devendo ocorrer o ressarcimento dos valores já pagos.</p>""",

    "9ª": """<p>Cláusula 9ª. Caso o CONTRATANTE requisite a rescisão imotivada do presente contrato, os valores pagos ao CONTRATADO serão restituídos mediante pagamento de multa no valor de 20% do valor total do contrato. Em caso de rescisão imotivada pelo CONTRATADO os valores já recebidos por este deverão ser ressarcidos à CONTRATANTE. Em ambos os casos a parte que der causa à rescisão imotivada está sujeita a eventuais danos materiais e/ou morais causados.</p>""",

    "10ª": """<p>Cláusula 10ª. O CONTRATADO assume o compromisso de realizar e entregar o serviço das fotografias em alta resolução dentro do prazo de 15 dias, a contar da data do ensaio fotográfico, de acordo com a forma estabelecida no presente contrato.</p>""",

    "11ª": """<p>Cláusula 11ª. O CONTRATANTE autoriza o uso de imagens do evento, para divulgação em site, mostruários, portfólios e anúncios comerciais, respeitando-se a integridade e a moralidade da CONTRATANTE.</p>
<p>Parágrafo Primeiro. Fica eleito o foro da comarca de Londrina, com exclusão de qualquer outro, por mais privilegiado que seja, para dirimir quaisquer devidas ou litígios oriundos deste contrato.</p>""",

    "12ª": """<p>Cláusula 12ª. Os cartões de memória etc. que serão utilizados são de exclusiva propriedade do CONTRATADO, não estando incluídos no orçamento. Não serão negociados e ficarão arquivados pelo tempo determinado de um ano para cópias e/ou ampliação eventualmente solicitadas pela CONTRATANTE, a preços atualizados e combinados no momento da solicitação.</p>""",

    "13ª": """<p>Cláusula 13ª. O CONTRATANTE tem o prazo de 5 dias a contar da data da entrega do material para solicitar qualquer alteração no material entregue, tendo um prazo de 30 dias para recebê-lo novamente. Após esse prazo, não será possível solicitar alterações.</p>""",

    "14ª": """<p>Cláusula 14ª. O CONTRATANTE confirma estar ciente da estética, estilo artístico fotográfico e características do formato de trabalho do CONTRATADO. O CONTRATANTE não poderá exigir características externas ao trabalho feito.</p>""",

    "15ª": """<p>Cláusula 15ª. Os arquivos originais serão armazenados por 30 dias, a contar a partir da data de entrega das fotografias digitais e/ou impressas. Os arquivos digitais entregues, serão armazenados por 1 ano, a contar a partir da data de entrega das fotografias digitais e/ou impressas.</p>"""
}

# Cláusulas padrão para contrato de evento
clausulas_evento = {
    "1ª": """<p>Cláusula 1ª. É objetivo do presente contrato a prestação do serviço de FOTOGRAFIA a cargo do CONTRATADO para o evento de {{ contrato.nome_evento }}, a se realizar no dia {{ contrato.data_evento }}, aproximadamente às {{ contrato.horario_evento }}, em {{ contrato.local_evento }}, {{ contrato.cidade_estado_evento }}.</p>""",

    "2ª": """<p>Parágrafo Único. A equipe CONTRATADA prestará o serviço de cobertura fotográfica por até {{ contrato.tempo_cobertura }} totais a partir do horário previsto para início do {{ contrato.nome_evento }}, com {{ contrato.qtd_fotografos }} FOTÓGRAFO(s) durante toda a cobertura fotográfica.</p>""",

    "3ª": """<p>Cláusula 2ª. O CONTRATANTE se compromete a disponibilizar o acesso da equipe de fotografia aos locais do evento e garantir condições adequadas para o trabalho, conforme acordado previamente.</p>""",

    "4ª": """<p>Cláusula 3ª. É de responsabilidade do CONTRATANTE informar à equipe fotográfica sobre momentos importantes e protocolos previamente definidos para o evento.</p>""",

    "5ª": """<p>Cláusula 4ª. O CONTRATADO deverá entregar ao CONTRATANTE o serviço conforme a proposta personalizada, que inclui os seguintes serviços:</p>
<p>{{ contrato.descricao_servico }}</p>""",

    "6ª": """<p>Cláusula 5ª. O CONTRATADO se compromete a fornecer ao CONTRATANTE a cópia deste contrato com todos os detalhes e especificidades da prestação do serviço contratado.</p>""",

    "7ª": """<p>Cláusula 6ª. O presente serviço será remunerado pela quantia de {{ contrato.valor }}.</p>
<p>Referente aos serviços efetivamente prestados conforme descrito na cláusula 4ª, cujo pagamento será efetuado da seguinte maneira:</p>
<p>{{ contrato.forma_pagamento }}</p>""",

    "8ª": """<p>Cláusula 7ª. A rescisão do presente contrato poderá ser solicitada por qualquer das partes em caso de motivo relevante, fortuito ou força maior. A parte interessada deverá comunicar a outra com antecedência mínima de 90 dias.</p>""",

    "9ª": """<p>Cláusula 8ª. Em caso de rescisão imotivada por parte do CONTRATANTE, será aplicada multa de 20% sobre o valor total contratado. Se a rescisão for por parte do CONTRATADO, este deverá devolver os valores recebidos.</p>""",

    "10ª": """<p>Cláusula 9ª. O CONTRATADO se compromete a realizar a entrega das fotografias em alta resolução no prazo de até 30 dias após a realização do evento.</p>""",

    "11ª": """<p>Cláusula 10ª. O CONTRATANTE autoriza o uso de imagens do evento para portfólio, mostruário, site ou redes sociais do CONTRATADO, desde que respeitada a integridade e imagem dos retratados.</p>""",

    "12ª": """<p>Parágrafo Único. Fica eleito o foro da comarca de Londrina para dirimir quaisquer conflitos oriundos deste contrato, com renúncia de qualquer outro por mais privilegiado que seja.</p>""",

    "13ª": """<p>Cláusula 11ª. Os cartões de memória e arquivos brutos são de propriedade do CONTRATADO e não estão incluídos no pacote contratado. O armazenamento será garantido por até 1 ano após a entrega final do material.</p>"""
}

clausulas_por_tipo = {
    "ensaio": clausulas_ensaio,
    "evento": clausulas_evento
}
