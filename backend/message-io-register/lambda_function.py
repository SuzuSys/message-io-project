import json
import boto3
import discord

BUCKET = 'message-io-bucket'
META_FILE = 'meta.json'
DATA_FILE = 'data.json'

s3_client = boto3.client('s3')

def load_meta():
    response = s3_client.get_object(Bucket=BUCKET, Key=META_FILE)
    body = response['Body'].read()
    meta_dict = json.loads(body.decode('utf-8'))
    return meta_dict

def save_data(data_dict):
    body = json.dumps(data_dict)
    s3_client.put_object(Body=body, Bucket=BUCKET, Key=DATA_FILE)

class DiscordClient(discord.Client):
    def __init__(self, meta):
        intents = discord.Intents.none()
        intents.guild_messages = True
        intents.guild_reactions = True
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        super().__init__(intents=intents)
        self.channels: list[dict] = meta["channels"]
        self.limit: int = meta["messages"]["limit"]
    
    async def find_messages(self, channel: discord.TextChannel):
        # sorted messages (latest first, id desc)
        all_messages: list[discord.Message] = [m async for m in channel.history(limit=self.limit)]
        messages_dict = []
        for message in all_messages:
            message_dict = {
                "id": str(message.id),
                "author": {
                    "id": str(message.author.id),
                    "name": message.author.name,
                    "display_name": message.author.display_name,
                    "nick": message.author.nick if isinstance(message.author, discord.Member) else None, 
                    "display_avatar": {
                        "key": message.author.display_avatar.key,
                        "url": message.author.display_avatar.url,
                        "animated": message.author.display_avatar.is_animated(),
                    },
                    "top_role": {
                        "id": str(message.author.top_role.id),
                        "name": message.author.top_role.name,
                        "color": str(message.author.top_role.color),
                    } if isinstance(message.author, discord.Member) else None,
                },
                "created_at": f'{message.created_at:%Y-%m-%d %H:%M:%S}',
                "edited_at": f'{message.edited_at:%Y-%m-%d %H:%M:%S}' if message.edited_at else None,
                "content": message.content,
                "attachments": [{
                    "id": str(attachment.id),
                    "url": attachment.url,
                    "filename": attachment.filename,
                    "content_type": attachment.content_type,
                } for attachment in message.attachments],
                "pinned": message.pinned,
                "reactions": [{
                    "count": reaction.count,
                    "emoji_obj": {
                        "id": str(reaction.emoji.id),
                        "url": reaction.emoji.url,
                        "animated": reaction.emoji.animated,
                    } if isinstance(reaction.emoji, (discord.Emoji, discord.PartialEmoji)) else reaction.emoji,
                    "users": [{
                        "id": str(user.id),
                        "name": user.name,
                        "display_name": user.display_name,
                        "nick": user.nick if isinstance(user, discord.Member) else None,
                        "display_avatar": {
                            "key": user.display_avatar.key,
                            "url": user.display_avatar.url,
                            "animated": user.display_avatar.is_animated(),
                        },
                        "top_role": {
                            "id": str(user.top_role.id),
                            "name": user.top_role.name,
                            "color": str(user.top_role.color),
                        } if isinstance(user, discord.Member) else None,
                    } async for user in reaction.users()],
                } for reaction in message.reactions],
                "stickers": [{
                    "id": str(sticker.id),
                    "name": sticker.name,
                    "url": sticker.url,
                } for sticker in message.stickers],
                "mentions": [{
                    "id": str(user.id),
                    "name": user.name,
                    "display_name": user.display_name,
                    "nick": user.nick if isinstance(user, discord.Member) else None,
                } for user in message.mentions],
                "channel_mentions": [{
                    "id": str(channel.id),
                    "name": channel.name,
                    "category": {
                        "id": str(channel.category.id),
                        "name": channel.category.name,
                    } if channel.category else None,
                } for channel in message.channel_mentions],
                "role_mentions": [{
                    "id": str(role.id),
                    "name": role.name,
                    "color": str(role.color),
                } for role in message.role_mentions],
                "embeds": [{
                    "url": embed.url,
                    "type": embed.type,
                } for embed in message.embeds],
                "reference": {
                    "id": str(message.reference.message_id),
                } if message.reference else None,
            }
            if message.reference and message.reference.message_id:
                referenced_message = await channel.fetch_message(message.reference.message_id)
                message_dict["reference"]["author"] = {
                    "id": str(referenced_message.author.id),
                    "name": referenced_message.author.name,
                    "display_name": referenced_message.author.display_name,
                    "nick": referenced_message.author.nick if isinstance(referenced_message.author, discord.Member) else None,
                    "display_avatar": {
                        "key": referenced_message.author.display_avatar.key,
                        "url": referenced_message.author.display_avatar.url,
                        "animated": referenced_message.author.display_avatar.is_animated(),
                    },
                    "top_role": {
                        "id": str(referenced_message.author.top_role.id),
                        "name": referenced_message.author.top_role.name,
                        "color": str(referenced_message.author.top_role.color),
                    } if isinstance(referenced_message.author, discord.Member) else None,
                }
                message_dict["reference"]["created_at"] = f'{referenced_message.created_at:%Y-%m-%d %H:%M:%S}'
                message_dict["reference"]["edited_at"] = f'{referenced_message.edited_at:%Y-%m-%d %H:%M:%S}' if referenced_message.edited_at else None
                message_dict["reference"]["content"] = referenced_message.content
                message_dict["reference"]["attachments"] = [{
                    "id": attachment.id,
                    "url": attachment.url,
                    "filename": attachment.filename,
                    "content_type": attachment.content_type,
                } for attachment in referenced_message.attachments]
                message_dict["reference"]["stickers"] = [{
                    "id": str(sticker.id),
                    "name": sticker.name,
                    "url": sticker.url,
                } for sticker in referenced_message.stickers]
            messages_dict.append(message_dict)
        return messages_dict

    async def on_ready(self):
        channels_dict = []
        for channel_meta in self.channels:
            channel_dict = {
                "id": str(channel_meta["id"])
            }
            channel = self.get_channel(channel_meta["id"])
            if isinstance(channel, discord.TextChannel):
                channel_dict["name"] = channel.name
                channel_dict["category"] = {
                    "id": str(channel.category.id),
                    "name": channel.category.name,
                } if channel.category else None
                channel_dict["guild"] = {
                    "id": str(channel.guild.id),
                    "name": channel.guild.name,
                }
                channel_dict["messages"] = await self.find_messages(channel)
            channels_dict.append(channel_dict)
        save_data(channels_dict)
        await self.close()

def lambda_handler(event, context):
    meta_dict = load_meta()
    DiscordClient(meta_dict).run(meta_dict["bot"]["token"])