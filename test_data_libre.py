
detect = {
    'good': [
        { 'q': 'What language is this?', },
        { 'q': 'Que idioma es?', },
    ],
    'bad': [],
}

translate = {
    'good': [
        { 'q': 'What language is this?', 'source': 'en', 'target': 'es', },
    ],
    'bad': [],
}

languages = {
    'good': [],
    'bad': [],
}

test_parameters = {
    '/detect': detect ,
    '/languages': languages ,
    '/translate': translate ,
} 

