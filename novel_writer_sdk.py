import os
from zai import ZaiClient
from config import ZAI_API_KEY

def save_chat_history(history):
    """将聊天记录保存到用户指定的txt文件中。"""
    if not history:
        print("当前没有聊天记录可以保存。")
        return

    while True:
        filename = input("请输入要保存的文件名 (例如: 第一章.txt): ").strip()
        if not filename:
            print("文件名不能为空，请重新输入。")
            continue
        
        if not filename.lower().endswith('.txt'):
            filename += '.txt'
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # 格式化输出，使其更像对话
                full_content = ""
                for message in history:
                    role = message['role']
                    content = message['content']
                    # 将 role 翻译成更友好的称呼
                    display_role = "你" if role == "user" else "AI"
                    full_content += f"[{display_role}]: {content}\n\n"
                
                f.write(full_content)
            print(f"\n✅ 聊天记录已成功保存到 {os.path.abspath(filename)}\n")
            break
        except IOError as e:
            print(f"[文件保存错误] {e}，请重试。")

def main():
    """主函数，程序的入口。"""
    print("--- 欢迎使用 z.ai 小说创作助手 (SDK版) ---")
    print("你可以直接输入你的想法或指令，输入 'save' 保存记录，输入 'exit' 退出程序。")
    
    # 初始化客户端，只需一次
    client = ZaiClient(api_key=ZAI_API_KEY)

    # 聊天历史记录，格式需要符合API要求
    chat_history = [
        {"role": "system", "content": "你是一位顶级的小说家，擅长根据用户的提示进行续写、扩写和创作。你的文笔优美，情节富有想象力。"}
    ]

    while True:
        user_input = input("\n>> 你: ").strip()

        if user_input.lower() == 'exit':
            print("感谢使用，再见！")
            break
        
        if user_input.lower() == 'save':
            # 保存时，我们排除system prompt
            save_chat_history(chat_history[1:])
            continue

        if not user_input:
            print("输入不能为空，请继续。")
            continue

        # 将用户输入添加到历史记录
        chat_history.append({"role": "user", "content": user_input})
        
        print("\n--- z.ai 正在思考中... ---\n")
        
        try:
            # 调用API，传入完整的聊天历史以保持上下文
            response = client.chat.completions.create(
                model="glm-4.5",  # 使用文档中推荐的模型
                messages=chat_history,
                thinking={"type": "enabled"}, # 启用思考模式，可能会得到更好的结果
                max_tokens=4096,
                temperature=0.8 # 创作小说可以适当提高创造性
            )
            
            # 从响应中提取AI回复
            ai_reply = response.choices[0].message.content.strip()
            
            print(f"\n>> AI: {ai_reply}\n")
            
            # 将AI的回复也添加到历史记录，以便下次对话能记住
            chat_history.append({"role": "assistant", "content": ai_reply})
            
        except Exception as e:
            print(f"\n[API调用出错] {e}\n")
            # 如果API调用失败，移除刚刚添加的用户输入，以免影响下次请求
            chat_history.pop()

        print("-" * 20)

if __name__ == "__main__":
    main()