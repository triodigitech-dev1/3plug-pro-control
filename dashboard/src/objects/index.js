import site from './site';
import group from './group';
import bench from './bench';
import server from './server';
import notification from './notification';
import accessRequests from './accessRequests';
import forensicEvent from './forensicEvent';

let objects = {
	Site: site,
	Group: group,
	Bench: bench,
	Server: server,
	Notification: notification,
	AccessRequests: accessRequests,
	'Forensic Event': forensicEvent,
};

export function getObject(name) {
	return objects[name];
}

export default objects;
