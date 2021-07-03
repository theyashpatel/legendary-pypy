const SubDomain = require('../models/subdomains')
const util = require('util');
const exec = util.promisify(require('child_process').exec);

const python_scripts_path = '/stuff/legendary-pypy/python-scripts/'

async function createSDScript(sd) {
try {
    const { stdout, stderr } = await exec(`${python_scripts_path}vhost-creator.py -c ${sd}`);
    console.log(stdout)
    console.log(stderr)
}catch (err){
    console.error(err);
};
};

async function deleteSDScript(sd) {
try {
    const { stdout, stderr } = await exec(`${python_scripts_path}vhost-creator.py -d ${sd}`);
    console.log(stdout)
    console.log(stderr)
}catch (err){
    console.error(err);
};
};

// create domain
const createSubDomain = async (req, res) => {
    const subDomain = await SubDomain.create(req.body)
    // run python script for creating subdomain
    createSDScript(subDomain.subdomain)
    res.status(201).json({subDomain})
}
// delete domain
const deleteSubDomain = async (req, res) => {
    const { sdomain } = req.params
    const sd = await SubDomain.findOneAndDelete({subdomain: sdomain})
    if (!sd) {
        return res.status(404).send('resource not found')
    }
    deleteSDScript(sd.subdomain)
    res.status(200).json({ sd })
}

module.exports = {
    createSubDomain,
    deleteSubDomain
}