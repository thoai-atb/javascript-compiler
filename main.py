import src as js_compiler

file_path = input('Enter an input file name to be executed: ')
result, error = js_compiler.run('input/' + file_path + '.js', 'input/' + file_path + '[log].txt')
if error:
    print(error.as_string())
else:
    pass
    # print(f'{result}')
