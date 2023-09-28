import hikari
import lightbulb
#.\env\Scripts\activate
bot=lightbulb.BotApp(
    token='',
    default_enabled_guilds=(937914803375185970)
)

@bot.command
@lightbulb.command('ping','Says pong!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")

################################################
#Tic Tac Toe
################################################
board=[[0 for i in range(3)] for j in range(3)]
#1-X
#-1-0
global currentPlayer
currentPlayer=1

@bot.command
@lightbulb.command('tictactoe','Tic Tac Toe')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def ticTacToe(ctx):
    pass

#current player
@ticTacToe.child
@lightbulb.command('currentplayer','get current player')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def getPlayer(ctx):
    if(currentPlayer==-1):
        await ctx.respond("0's turn")
    else:
        await ctx.respond("X's turn")

#player move
@ticTacToe.child
@lightbulb.option('row',"1-3", type=int)
@lightbulb.option('col',"1-3",type=int)
@lightbulb.command("playermove","Enter row and column")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def playerMove(ctx):
    if(win(board)!=0):
        await ctx.respond("Game is Over")
        return None
    r=ctx.options.row-1
    c=ctx.options.col-1
    if(r<0 or r>2 or c<0 or c>2):
        await ctx.respond("Invalid move")
        return
    if(board[r][c]!=0):
        await ctx.respond("Invalid move") 
        return
    global currentPlayer
    board[r][c]=currentPlayer
    currentPlayer*=-1
    await ctx.respond("Move Completed!")
    await ctx.respond(makeBoard(board))
    winStatus=win(board)
    if(winStatus!=0):
        if(winStatus==-1):
            await ctx.respond("0 wins")
        else:
            await ctx.respond("X wins")
        return None
    if(currentPlayer==-1):
        await ctx.respond("0's turn")
    else:
        await ctx.respond("X's turn")

#check for winner
def win(board):
    for i in range(0,3):
        if(board[i][0]==board[i][1] and board[i][1]==board[i][2]):
            return board[i][0]
    for j in range(0,3):
        if(board[0][j]==board[1][j] and board[1][j]==board[2][j]):
            return board[0][j]
    if(board[0][0]==board[1][1] and board[1][1]==board[2][2]):
        return board[0][0]
    if(board[2][0]==board[1][1] and board[1][1]==board[0][2]):
        return board[2][0]
    return 0


#reset game
@ticTacToe.child
@lightbulb.command('reset',"Reset the game")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def resetBoard(ctx):
    for i in range(0,3):
        for j in range(0,3):
            board[i][j]=0
    await ctx.respond("Game Reset")

#print the board
@ticTacToe.child
@lightbulb.command('board','View the game board')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def viewBoard(ctx):
    await ctx.respond(makeBoard(board))

def makeBoard(board):
    result='|'
    for i in range(len(board)):
        for col in board[i]:
            result+=" "
            if(col==1):
                result+="X"
            elif(col==-1):
                result+="0"
            else:
                result+="#"
            result+=" "
            result+="|"
        if(i<2):
            result+="\n=======\n"
            result+="|"
    return result

bot.run()
