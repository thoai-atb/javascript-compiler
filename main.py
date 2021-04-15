import javascript_compiler.runner as runner

file_name = 'input.js'
text = open(file_name, 'r').read()
result, error = runner.run(file_name, text)
if error:
    print(error.as_string())
else:
    print(result)
