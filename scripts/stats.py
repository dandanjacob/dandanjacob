import os
from github import Github

# Autenticação (token vem do GitHub Actions secrets)
token = os.getenv("PERSONAL_TOKEN")
username = os.getenv("GITHUB_ACTOR")

g = Github(token)
user = g.get_user(username)

# Total de repositórios contribuídos
repos_contributed = len(list(user.get_repos()))

# Contar commits, PRs e linhas (simplificado)
total_commits = 0
total_prs = 0
total_additions = 0
total_deletions = 0

for repo in user.get_repos():
    try:
        # PRs
        total_prs += repo.get_pulls(state="all").totalCount

        # Commits (apenas se você for colaborador/owner)
        total_commits += repo.get_commits(author=user).totalCount

        # Linhas adicionadas/removidas (últimos 100 commits)
        for commit in repo.get_commits(author=user)[:100]:
            stats = commit.stats
            total_additions += stats.additions
            total_deletions += stats.deletions

    except Exception:
        continue

# Bloco de Markdown
output = f"""
### 📊 Minhas estatísticas no GitHub

- 🔥 Total de commits: **{total_commits}**
- 🚀 Pull Requests abertos: **{total_prs}**
- 📦 Repositórios contribuídos: **{repos_contributed}**
- ➕ Linhas adicionadas: **{total_additions}**
- ➖ Linhas removidas: **{total_deletions}**
"""

print(output)
