const mongoose = require('mongoose')

const connectDB = (url) => {
    return mongoose.connect(process.env.MONGO_URI,{
        useFindAndModify: false,
        useCreateIndex: true,
        useNewUrlParser: true,
        useUnifiedTopology: true
    })
}

module.exports = connectDB