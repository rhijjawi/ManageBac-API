const fetch = require('node-fetch');
const cheerio = require('cheerio');
const cal = { "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12, }

/**
 * 
 * @param {string} domain Your Managebac Domain! 
 * @param {string} token Your Managebac Token (Also known as _managebac_session cookie)
 * @returns Returns Javascript Object with deadlines and tasks.
 * 
 * @example
 * 
 * await mbapi("IBS", "o1h98dh93hr2r32d...")
 */
async function mbapi(domain, token) {
    let i = 1;
    const tasksArr = [];
    const deadlinesArrr = [];
    let name;
    do {
        let req;
        try {
            req = await fetch(`https://kaust.managebac.com/student/tasks_and_deadlines?upcoming_page=${i}`, {
                headers: {
                    cookie: `_managebac_session=${token}`
                }
            });
        } catch (err) {
            console.log(err)
        }
        if (req.status === 404) {
            throw new Error('BAD_URL_ERR: This URL does not exist on Managebac\'s servers! Please check if you put in the correct domain address!')
        }
        if (req.status === 401) {
            throw new Error('BAD_TOKEN_ERR: You used a token which is invalid or expired! Please check if you used the correct token!')
        }
        const $ = cheerio.load(await req.text());
        name = $('title').text().split('| ')[1].replace('Classes', '');
        const tasks = $('div').find('.line', '.task-node anchor', '.js-presentation').toArray();
        const deadlines = $('div').find('.line').toArray();
        tasks.forEach((task) => {
            const day = $(task).find('.day').text();
            const month = $(task).find('.month').text();
            const title = $(task).find('h3', '.title', 'a').text().replace(/\r?\n|\r/g, "")
            const link = $(task).find('a').attr('href')
            const id = link.split('core_tasks/')[1]
            const obj = {
                id: id,
                link: `https://${domain}.managebac.com${link}`,
                title: title,
                dueDate: `${day}/${cal[month]}`
            }
            tasksArr.push(obj)
        });
        deadlines.forEach((dl) => {
            let title = $(dl).find("h4", ".title");
            if (title) {
                title = $(title).find('a').text();
                const timestamp = $(dl).find('.date-badge');
                const day = $(timestamp).find(".day").text();
                const month = $(timestamp).find('.month').text();
                const link = $(dl).find('a').attr('href');
                if (!link.includes('events/')) return;
                const id = link.split('events/')[1];
                const obj = {
                    id,
                    link: `https://${domain}.managebac.com${link}`,
                    title,
                    dueDate: `${day}/${cal[month]}`
                }
                deadlinesArrr.push(obj);
            }
        })
        i++;
    } while (i <= 4);
    return {
        studentName: name,
        deadlines: deadlinesArrr,
        tasks: tasksArr,
    }
}

module.exports = mbapi();