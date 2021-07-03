const express = require('express')
const app = express()
const connectDB = require('./db/connect')
const subDomainRoutes = require('./routes/subdomains')
const notFound = require('./middleware/not-found')

require('dotenv').config()

app.use(express.json())
app.use('/api/v1/subdomains', subDomainRoutes)
app.use(notFound)


const PORT = process.env.PORT || 5000
const start = async () => {
    try {
        await connectDB(process.env.MONGO_URI)
            app.listen(PORT, () => {
            console.log(`Listening on port: ${PORT}`)
        })
    } catch (error) {
        console.log(error)        
    }
}

start()