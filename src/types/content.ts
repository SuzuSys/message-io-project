export interface RegContent {
  regexp: RegExp;
  format: (str: string) => string;
}
export interface ListStruct {
  content: string;
  currentArray: Array<ListStruct>;
  child?: Array<ListStruct>;
  parent?: ListStruct;
  firstNumber?: number; // If the list is ol, this type is number. If ul, then undefined.
}
export interface MentionReg {
  regexp: RegExp;
  display: string;
}
export interface Reg {
  italics: RegContent;
  bold: RegContent;
  boldItalics: RegContent;
  underline: RegContent;
  underlineItalics: RegContent;
  underlineBold: RegContent;
  underlineBoldItalics: RegContent;
  strickthrough: RegContent;
  links: {
    regexp: RegExp;
    file?: string;
  };
  maskedLinks: {
    regexp: RegExp;
    display: string;
    url: string;
  };
  codeBlock: RegContent;
  codeInline: RegContent;
  spoilerTag: RegContent;
  ul: {
    regexp: RegExp;
    li: Array<ListStruct>;
  };
  ol: {
    regexp: RegExp;
    li: Array<ListStruct>;
  };
  h1: RegContent;
  h2: RegContent;
  h3: RegContent;
  blockQuotes: {
    regexp: RegExp;
    content: Array<string>;
  };
  channelMention: MentionReg;
  roleMention: MentionReg;
  memberMention: MentionReg;
  everyoneMention: {
    regexp: RegExp;
  };
  hereMention: {
    regexp: RegExp;
  };
}
