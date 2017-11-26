const spawn = require('child_process').spawn

const callPython = (file, message, cb, err) => {
    const child = spawn('python', [file])
    let input = {}
    let errorMsg = ''

    // if data from stdout is not parseable, ignore it
    child.stdout.on('data', data => {
        try {
            input = JSON.parse(data.toString())
        } catch(e) {}
    })
    child.stderr.on('data', data => errorMsg += data.toString() + "\n")
    child.on('exit', exitCode => {
        if (exitCode !== 0) {
            err(exitCode, errorMsg)
        } else {
            cb(input)
        }
    })
    child.stdin.write(JSON.stringify(message))
    child.stdin.end()
}

const promisified = (cb) => {
    return (file, message) => {
        return new Promise((resolve, reject) => {
            cb(file,
               message,
               result => resolve(result),
               (exitCode, error) => reject({ exitCode, error }))
        })
    }
}

module.exports = promisified(callPython)