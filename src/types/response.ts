export interface Channel {
  id: string;
  name: string;
  guild: {
    id: string;
    name: string;
  };
  category: null | {
    id: string;
    name: string;
  };
  messages: Message[];
}

export interface IncompleteChannel {
  id: string;
}

export interface Message {
  id: string;
  author: {
    id: string;
    name: string;
    display_name: string;
    nick: null | string;
    display_avatar: {
      key: string;
      url: string;
      animated: boolean;
    };
    top_role: null | {
      id: string;
      name: string;
      color: string;
    };
  };
  created_at: string;
  edited_at: null | string;
  content: string;
  attachments: {
    id: string;
    url: string;
    filename: string;
    content_type: null | string;
  }[];
  pinned: boolean;
  reactions: {
    count: number;
    emoji_obj:
      | {
          id: null | string;
          url: string;
          animated: boolean;
        }
      | string;
    users: {
      id: string;
      name: string;
      display_name: string;
      nick: null | string;
      display_avatar: {
        key: string;
        url: string;
        animated: boolean;
      };
      top_role: null | {
        id: string;
        name: string;
        color: string;
      };
    }[];
  }[];
  stickers: {
    id: string;
    name: string;
    url: string;
  }[];
  mentions: {
    id: string;
    name: string;
    display_name: string;
    nick: null | string;
  }[];
  channel_mentions: {
    id: string;
    name: string;
    category: null | {
      id: string;
      name: string;
    };
  }[];
  role_mentions: {
    id: string;
    name: string;
    color: string;
  }[];
  embeds: {
    url: string | null;
    type: 'rich' | 'image' | 'video' | 'gifv' | 'article' | 'link';
    thumbnail: null | {
      url: null | string;
      width: null | number;
      height: null | number;
    };
    title: null | string;
    description: null | string;
    provider: null | {
      name: null | string;
      url: null | string;
    };
  }[];
  reference:
    | null
    | {
        id: null | string;
      }
    | {
        id: string;
        author: {
          id: string;
          name: string;
          display_name: string;
          nick: null | string;
          display_avatar: {
            key: string;
            url: string;
            animated: boolean;
          };
          top_role: null | {
            id: string;
            name: string;
            color: string;
          };
        };
        created_at: string;
        edited_at: null | string;
        content: string;
        attachments: {
          id: string;
          url: string;
          filename: string;
          content_type: null | string;
        }[];
        stickers: {
          id: string;
          name: string;
          url: string;
        }[];
      };
}
