const mongoose = require('mongoose')

const SubDomainSchema = new mongoose.Schema({
    subdomain: {
        type: String,
        required: [true, 'subdomain is required'],
        maxlength: [26, 'name cannot be more than 26 characters'],
        trim: true
    }
})


module.exports = mongoose.model('SubDomain', SubDomainSchema)