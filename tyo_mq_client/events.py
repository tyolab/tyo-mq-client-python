#
#
from .constants import Constants
    # public static string to_event_string(string event_name, string? prefix = null, string? suffix = null) {
        
    #     // eventStr = event
    #     // TODO
    #     // if (typeof event === "string") {
    #     //     eventStr = event
    #     // }
    #     // else if (typeof event === "object" && event.event) {
    #     //     eventStr = event.event
    #     // }
    #     // else 
    #     //     throw new Error ("Unknown event object: should be a string or object with event string")
    #     // return eventStr
    #     return (null != prefix ? (prefix + '-') : "") + event_name + (null != suffix ? ('-' + suffix) : "");;
    # }

    # public static string to_consume_event(string event_name) {
    #     return to_event_string(event_name, "CONSUME");
    # }

    # public static string to_consumer_event(string event_name, string prefix, bool is_all = false) {
    #     if (is_all)
    #         return to_event_string(event_name, prefix.lower());
    #     return to_event_string(event_name, prefix).lower();
    # }

    # public static string to_ondisconnect_event(string id) {
    #     return to_event_string(id, "DISCONNECT");
    # }

    # public static string to_onunsubscribe_event(string event_name, string id) {
    #     // string eventStr = to_event_string(event_name);
    #     // return "UNSUBSCRIBE-" + eventStr + "-" + id;
    #     return to_event_string(event_name, "UNSUBSCRIBE", id);
    # }

    # public static string to_onsubscribe_event(string id) {
    #     // return "SUBSCRIBE-TO" + ("-" + id != null ? id : "");
    #     return to_event_string("TO", "SUBSCRIBE", id);
    # }

    # public static string to_consume_all_event(string producer) {
    #     return to_event_string("CONSUME") + to_consumer_all_event(producer);
    # }

    # public static string to_consumer_all_event (string producer) {
    #     // return 'producer + "-ALL";
    #     return to_event_string(producer.lower(), null, Constants.EVENT_ALL);
    # }

class Events(object):
    #
    @staticmethod
    def to_event_string(event_name, prefix = None, suffix = None):
        # eventStr = event
        # TODO
        # if (typeof event === 'string') {
        #     eventStr = event
        # }
        # else if (typeof event === 'object' && event.event) {
        #     eventStr = event.event
        # }
        # else 
        #     throw new Error ('Unknown event object: should be a string or object with event string')
        return ('' if (prefix is None) else (prefix + '-')) + event_name + ('' if (suffix is None) else ('-' + suffix))

    @staticmethod
    def to_consume_event(event):
        return Events.to_event_string(event, 'CONSUME')
    
    @staticmethod
    def to_consumer_event(event_name, prefix = None, is_all = False):
        if (is_all is True):
            return Events.to_event_string(event_name, (None if (prefix is None) else prefix.lower()))
        return Events.to_event_string(event_name, prefix).lower()

    @staticmethod
    def to_ondisconnect_event(id):
        # return 'DISCONNECT-' + id
        return Events.to_event_string(id, 'DISCONNECT')

    @staticmethod
    def to_onunsubscribe_event(event, id):
        # eventStr = Events.to_event_string(event)
        # return 'UNSUBSCRIBE-' + eventStr + '-' + id
        return Events.to_event_string(event, 'UNSUBSCRIBE', id)

    @staticmethod
    def to_onsubscribe_event(id):
        # return 'SUBSCRIBE-TO' + ("-" + id if (id is not None) else "")
        return Events.to_event_string('TO', 'SUBSCRIBE', id)
    
    @staticmethod
    def to_consumer_all_event (producer):
        # return 'producer + "-ALL"
        return Events.to_event_string(producer.lower(), None, Constants.EVENT_ALL)