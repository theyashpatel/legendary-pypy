const express = require('express')
const router = express.Router()
const { createSubDomain, deleteSubDomain} = require('../controllers/subdomains')

router.route('/').post(createSubDomain)
router.route('/:sdomain').delete(deleteSubDomain)

module.exports = router