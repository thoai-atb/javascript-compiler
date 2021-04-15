import src as js_compiler

file_name = 'input.js'
text = open(file_name, 'r').read()
result, error = js_compiler.run(file_name, text)
if error:
    print(error.as_string())
else:
    print(result)
