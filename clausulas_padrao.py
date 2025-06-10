# Cláusulas padrão para contrato de ensaio
clausulas_ensaio = {
    "1ª": """<p>Cláusula 1ª. É objetivo do presente contrato a prestação do serviço de FOTOGRAFIA a cargo do CONTRATADO para o ENSAIO FOTOGRÁFICO, a se realizar no dia {{ contrato.data_ensaio }}, aproximadamente às {{ contrato.horario_ensaio }}, em {{ contrato.cidade_estado_ensaio }}.</p>""",

    "2ª": """<p>Cláusula 2ª. O CONTRATANTE deverá comparecer ao local agendado para realização do ensaio fotográfico no horário especificado previamente, sendo permitida uma tolerância de 30 minutos antes ou depois do horário especificado previamente.</p><p>Cláusula 2ª. O CONTRATANTE deverá comparecer ao local agendado para realização do ensaio fotográfico no horário especificado previamente, sendo permitida uma tolerância de 30 minutos antes ou depois do horário especificado previamente.</p>""",

    "3ª": """<p>Cláusula 3ª. Atrasos superiores a 30 minutos do horário especificado previamente, sem aviso prévio de 1 hora antes do horário agendado, será necessário reagendar a sessão fotográfica.</p>""",

    "4ª": """<p>Cláusula 4ª. O CONTRATANTE deverá efetuar o pagamento na forma e condições estabelecidas na cláusula 7ª.</p>""",

    "5ª": """<p>Cláusula 5ª. O CONTRATADO entregará ao CONTRATANTE o serviço com os seguintes itens:</p>
    <p>{{ contrato.descricao_servico }}</p>""",

    "6ª": """<p>Cláusula 6ª. É dever do CONTRATADO fornecer ao CONTRATANTE, a cópia do contrato, contendo todas as especificidades da prestação de serviço contratado.</p>""",

    "7ª": """<p>Cláusula 7ª. O presente serviço será remunerado pela quantia de {{ contrato.valor }} Referente aos serviços efetivamente prestados pelo pacote personalizado citado na cláusula5ª, cujo pagamento será efetuado da seguinte maneira:</p>
    <p> {{ contrato.forma_pagamento }}</p>""",

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
    "1ª": """<p>Cláusula 1ª. É objetivo do presente contrato a prestação do serviço de FOTOGRAFIA a cargo do CONTRATADO para o evento {{ contrato.nome_evento }}, a se realizar no dia {{ contrato.data_evento }}, aproximadamente às {{ contrato.horario_evento }}, em {{ contrato.local_evento }}, {{ contrato.cidade_estado_evento }}.</p>
    <p>Parágrafo Único. A equipe CONTRATADA prestará o serviço de cobertura fotográfica por até {{ contrato.tempo_cobertura }} horas totais a partir do horário previsto para início do evento, com {{ contrato.qtd_fotografos }} fotógrafo(s).</p>""",

    "2ª": """<p>Cláusula 2ª. O CONTRATANTE deverá fornecer ao CONTRATADO, todas as informações necessárias à realização do serviço, devendo especificar os detalhes necessários à perfeita consecução do mesmo, e a forma como ele deve ser entregue, como: nome legível e identificação das pessoas de destaque; livre acesso da equipe ao local do evento; verificar a existência de pontos de energia para os equipamentos (iluminação, recarga de baterias para as câmeras, notebook, etc.); reservar uma mesa para a equipe se instalar e prover a alimentação do contratado.</p>""",

    "3ª": """<p>Cláusula 3ª . O CONTRATANTE deverá efetuar o pagamento na forma e condições estabelecidas na cláusula 6ª.</p>""",

    "4ª": """<p>Cláusula 4ª. O CONTRATADO deverá entregar ao CONTRATANTE o SERVIÇO DE FOTOGRAFIA referente ao a proposta personalizada para o CONTRATANTE, que inclui os seguintes serviços:</p>
    <p>{{ contrato.descricao_servico }}</p>""",

    "5ª": """<p>Cláusula 5ª. É dever do CONTRATADO fornecer ao CONTRATANTE, a cópia do contrato, contendo todas as especificidades da prestação de serviço contratado.</p>""",

    "6ª": """<p>Cláusula 6ª. O presente serviço será remunerado pela quantia de {{ contrato.valor }}. Referenteaos serviços efetivamente prestados pelo pacote personalizado citado na cláusula 4ª, cujo pagamento será efetuado da seguinte maneira:</p>
    <p>{{ contrato.forma_pagamento }}</p>""",

    "7ª": """<p>Cláusula 7ª. Poderá o presente instrumento ser rescindido por qualquer uma das partes em caso de motivo relevante, fortuito ou força maior, não obstante a outra parte deverá ser avisada previamente no prazo de 90 (noventa) dias, antes do evento, devendo ocorrer o ressarcimento dos valores já pagos.</p>""",

    "8ª": """<p>Cláusula 8ª. Caso o CONTRATANTE requisite a rescisão imotivada do presente contrato, os valores pagos ao CONTRATADO serão restituídos mediante pagamento de multa no valor de 20% do valor total do contrato. Em caso de rescisão imotivada pelo CONTRATADO os valores já recebidos por este deverão ser ressarcidos à CONTRATANTE. Em ambos os casos a parte que der causa à rescisão imotivada está sujeita a eventuais danos materiais e/ou morais causados.</p>""",

    "9ª": """<p>Cláusula 9ª. O CONTRATADO assume o compromisso de realizar e entregar o serviço das fotografias em alta resolução dentro do prazo de 30 dias, a contar da data do evento, de acordo com a forma estabelecida no presente contrato.</p>""",

    "10ª": """<p>Cláusula 10ª. Fica compactuada entre as partes a total inexistência de vínculo trabalhista entre as partes, excluindo as obrigações previdenciárias e os encargos sociais, não havendo entre CONTRATADO e CONTRATANTE qualquer tipo de relação de subordinação.</p>""",

    "11ª": """<p>Cláusula 11ª. Salvo com a expressa autorização do CONTRATANTE, não pode o CONTRATADO transferir ou subcontratar os serviços previstos neste instrumento, sob o risco de ocorrer rescisão imediata.</p>""",

    "12ª": """<p>Cláusula 12ª. O CONTRATANTE autoriza o uso de imagens do evento, para divulgação em site, mostruários, portfólios e anúncios comerciais, respeitando-se a integridade e a moralidade da CONTRATANTE.</p>
    <p>Parágrafo Primeiro. Fica eleito o foro da comarca de Londrina, com exclusão de qualquer outro, por mais privilegiado que seja, para dirimir quaisquer devidas ou litígios oriundos deste contrato.</p>""",

    "13ª": """<p>Cláusula 13ª. Os cartões de memória etc. que serão utilizados são de exclusiva propriedade do CONTRATADO, não estando incluídos no orçamento. Não serão negociados e ficarão arquivados pelo tempo determinado de um ano para cópias e/ou ampliação eventualmente solicitadas pela CONTRATANTE, a preços atualizados e combinados no momento da solicitação.</p>""",

    "14ª": """<p>Cláusula 14ª. A tolerância de qualquer das contratantes quanto a qualquer violação a dispositivos deste contrato será sempre entendida como mera liberalidade, não constituindo novação, não gerando, portanto, qualquer direito oponível pelas partes nem a perda da prerrogativa em exigir, de lado a lado, o pleno cumprimento das obrigações avençadas e a reparação de qualquer dano. E por acharem em perfeito acordo, em tudo quanto neste instrumento particular foi lavrado, obrigam-se a cumprir o presente contrato, assinando-o em duas vias de igual teor.</p>""",

    "15ª": """<p>Cláusula 15ª . O CONTRATANTE tem o prazo de 5 dias a contar da data da entrega do material para solicitar qualquer alteração no material entregue, tendo um prazo de 30 dias para recebê-lo novamente. Após esse prazo, não será possível solicitar alterações.</p>""",

    "16ª": """<p>Cláusula 16ª. O CONTRATANTE confirma estar ciente da estética, estilo artístico fotográfico e características do formato de trabalho do CONTRATADO. O CONTRATANTE não poderá exigir características externas ao trabalho feito.</p>""",

    "17ª": """<p>Cláusula 17ª. Os arquivos originais serão armazenados por 30 dias, a contar a partir da data de entrega das fotografias digitais e/ou impressas. Os arquivos digitais entregues, serão armazenados por 1 ano, a contar a partir da data de entrega das fotografias digitais e/ou impressas.</p>"""
}

clausulas_por_tipo = {
    "ensaio": clausulas_ensaio,
    "evento": clausulas_evento
}
