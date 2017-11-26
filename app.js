const express = require('express')
const path = require('path')
const fs = require('fs')

const callPython = require('./callPython')

const main = () => {
    const app = express()

    app.get('/', async (req, res) => {
        const training = path.resolve('sqcd', 'temp', '.gitkeep')
        const test = path.resolve('sqcd', 'temp', '.gitkeep')
        try {
            const data = await callPython('./sqcd/main.py', [training, test])
            res.json(data)
        } catch({ exitCode, error }) {
            console.error(`error for exit code ${exitCode} occurred in python submodule:\n${error}`)
            res.status(500).end()
        }
    })

    app.listen(3000, () => console.log('Listening on 3000'))
}

module.exports = main