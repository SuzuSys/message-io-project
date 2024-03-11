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
  messages: Array<Message>;
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
  attachments: Array<{
    id: string;
    url: string;
    filename: string;
    content_type: null | string;
  }>;
  pinned: boolean;
  reactions: Array<{
    count: number;
    emoji_obj:
      | {
          id: null | string;
          url: string;
          animated: boolean;
        }
      | string;
    users: Array<{
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
    }>;
  }>;
  stickers: Array<{
    id: string;
    name: string;
    url: string;
  }>;
  mentions: Array<{
    id: string;
    name: string;
    display_name: string;
    nick: null | string;
  }>;
  channel_mentions: Array<{
    id: string;
    name: string;
    category: null | {
      id: string;
      name: string;
    };
  }>;
  role_mentions: Array<{
    id: string;
    name: string;
    color: string;
  }>;
  embeds: Array<{
    url: string | null;
    type: 'rich' | 'image' | 'video' | 'gifv' | 'article' | 'link';
    image: null | {
      url: string | null;
      width: number | null;
    };
  }>;
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
        attachments: Array<{
          id: string;
          url: string;
          filename: string;
          content_type: null | string;
        }>;
        stickers: Array<{
          id: string;
          name: string;
          url: string;
        }>;
      };
}
