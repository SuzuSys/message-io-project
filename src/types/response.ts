export interface Channel {
  id: number;
  name: string;
  guild: {
    id: number;
    name: string;
  };
  category: null | {
    id: number;
    name: string;
  };
  messages: Array<Message>
}

export interface IncompleteChannel {
  id: number;
}

export interface Message {
  id: number;
  author: {
    id: number;
    name: string;
    display_name: string;
    nick: null | string;
    display_avatar: {
      key: string;
      url: string;
      animated: boolean;
    };
    roles: null | Array<{
      id: number;
      name: string;
      color: string;
    }>;
  };
  created_at: string;
  edited_at: null | string;
  content: string;
  attachments: Array<{
    url: string;
    filename: string;
    content_type: null | string;
  }>;
  pinned: boolean;
  reactions: Array<{
    count: number;
    emoji_obj: {
      id: null | number;
      url: string;
      animated: boolean;
    } | string;
    users: Array<{
      id: number;
      name: string;
      display_name: string;
      nick: null | string;
    }>
  }>;
  stickers: Array<{
    id: number;
    name: string;
    url: string;
  }>;
  reference: null | {
    id: null | number;
  } | {
    id: number;
    author: {
      id: number;
      name: string;
      display_name: string;
      nick: null | string;
      display_avatar: {
        key: string;
        url: string;
        animated: boolean;
      };
    };
    created_at: string;
    edited_at: null | string;
    content: string;
    attachments: Array<{
      url: string;
      filename: string;
      content_type: null | string;
    }>;
    stickers: Array<{
      id: number;
      name: string;
      url: string;
    }>;
  };
}
