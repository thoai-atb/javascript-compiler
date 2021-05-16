import src as js_compiler
result, error = js_compiler.run('input.js', 'log.txt')
if error:
    print(error.as_string())
else:
    pass
    # print(f'{result}')
