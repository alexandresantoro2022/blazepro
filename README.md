# 🍕 DeliveryPro - Sistema Completo de Delivery

Sistema profissional de delivery similar ao iFood, desenvolvido com Python, FastAPI e SQLAlchemy.

## 🚀 Funcionalidades

### **Múltiplos Tipos de Usuário**
- **Cliente**: Navegar restaurantes, fazer pedidos, rastrear entregas
- **Restaurante**: Gerenciar cardápio, receber e processar pedidos
- **Entregador**: Aceitar entregas, atualizar status de entrega
- **Admin**: Visualizar todos os pedidos e restaurantes do sistema

### **Gestão de Restaurantes**
- Cadastro completo de restaurantes
- Gerenciamento de cardápio com categorias
- Configuração de taxa de entrega e pedido mínimo
- Status de abertura/fechamento

### **Sistema de Pedidos**
- Carrinho de compras interativo
- Cálculo automático de preços e taxas
- Múltiplas formas de pagamento (Dinheiro, Cartão, PIX)
- Rastreamento de status em tempo real
- Atribuição automática de entregadores

### **Autenticação e Segurança**
- Sistema JWT para autenticação
- Hash de senhas com bcrypt
- Proteção de rotas por tipo de usuário
- Cookies HTTP-only para sessões

## 📋 Requisitos

- Python 3.9+
- pip

## 🔧 Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Iniciar o servidor:**
```bash
python main.py
```

O servidor estará disponível em: **http://localhost:8001**

## 👥 Contas de Teste

O sistema já vem com dados de teste pré-carregados:

### Admin
- **Email:** admin@deliverypro.com
- **Senha:** admin123

### Clientes
- **Email:** cliente1@email.com até cliente10@email.com
- **Senha:** 123456

### Restaurantes
- **Email:** restaurante1@email.com até restaurante3@email.com
- **Senha:** 123456

### Entregadores
- **Email:** entregador1@email.com até entregador5@email.com
- **Senha:** 123456

## 🏪 Restaurantes Disponíveis

1. **Pizzaria Bella Napoli**
   - Pizzas artesanais
   - Taxa de entrega: R$ 8,00
   - Pedido mínimo: R$ 25,00

2. **Burger House**
   - Hambúrgueres artesanais
   - Taxa de entrega: R$ 6,00
   - Pedido mínimo: R$ 20,00

3. **Sushi Master**
   - Culinária japonesa
   - Taxa de entrega: R$ 10,00
   - Pedido mínimo: R$ 35,00

## 📱 Fluxo de Uso

### Como Cliente:
1. Acesse a página inicial
2. Navegue pelos restaurantes disponíveis
3. Clique em "Ver Cardápio"
4. Adicione itens ao carrinho
5. Finalize o pedido (necessário login)
6. Acompanhe o status no dashboard

### Como Restaurante:
1. Faça login com conta de restaurante
2. Crie seu restaurante (se ainda não tiver)
3. Adicione itens ao cardápio
4. Receba e processe pedidos
5. Atualize status: Confirmar → Preparando → Pronto

### Como Entregador:
1. Faça login com conta de entregador
2. Veja pedidos disponíveis para entrega
3. Aceite uma entrega
4. Marque como entregue quando concluir

### Como Admin:
1. Faça login com conta admin
2. Visualize todos os pedidos do sistema
3. Monitore restaurantes cadastrados
4. Acesse estatísticas gerais

## 🗂️ Estrutura do Projeto

```
/vercel/sandbox/
├── main.py                 # Aplicação FastAPI principal
├── database.py             # Configuração do banco de dados
├── models.py               # Modelos SQLAlchemy
├── auth.py                 # Sistema de autenticação JWT
├── seed_data.py            # Dados iniciais do sistema
├── requirements.txt        # Dependências Python
├── delivery.db             # Banco de dados SQLite
├── crud/                   # Operações CRUD
│   ├── users.py
│   ├── restaurants.py
│   └── orders.py
├── templates/              # Templates HTML
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── restaurant_detail.html
│   ├── dashboard_customer.html
│   ├── dashboard_restaurant.html
│   ├── dashboard_driver.html
│   └── dashboard_admin.html
└── static/
    └── css/
        └── style.css       # Estilos CSS
```

## 🛠️ Tecnologias Utilizadas

- **Backend:** FastAPI 0.104.1
- **ORM:** SQLAlchemy 2.0.23
- **Banco de Dados:** SQLite (desenvolvimento)
- **Autenticação:** JWT (python-jose)
- **Hash de Senhas:** bcrypt
- **Templates:** Jinja2
- **Servidor:** Uvicorn

## 🎨 Design

- Interface moderna e responsiva
- Gradientes e animações suaves
- Design mobile-first
- Paleta de cores profissional
- Ícones emoji para melhor UX

## 📊 Status dos Pedidos

- **PENDING:** Aguardando confirmação do restaurante
- **CONFIRMED:** Confirmado pelo restaurante
- **PREPARING:** Em preparação
- **READY:** Pronto para entrega
- **IN_DELIVERY:** Saiu para entrega
- **DELIVERED:** Entregue
- **CANCELLED:** Cancelado

## 🔐 Segurança

- Senhas criptografadas com bcrypt
- Tokens JWT com expiração de 7 dias
- Cookies HTTP-only
- Validação de entrada com Pydantic
- Proteção contra SQL injection (SQLAlchemy)

## 🚀 Próximas Funcionalidades

- [ ] Integração com API de mapas
- [ ] Cálculo de distância real
- [ ] Sistema de avaliações
- [ ] Chat em tempo real
- [ ] Notificações push
- [ ] Pagamento online real
- [ ] Upload de imagens
- [ ] Relatórios e analytics

## 📝 API Endpoints

### Autenticação
- `POST /login` - Login de usuário
- `POST /register` - Cadastro de usuário
- `GET /logout` - Logout

### Restaurantes
- `GET /` - Lista de restaurantes
- `GET /restaurant/{id}` - Detalhes do restaurante
- `POST /restaurant/create` - Criar restaurante
- `GET /api/restaurants` - API JSON de restaurantes

### Pedidos
- `POST /order/create` - Criar pedido
- `POST /order/{id}/update-status` - Atualizar status
- `POST /order/{id}/assign-driver` - Atribuir entregador
- `GET /api/orders/my` - Meus pedidos (API)

### Dashboard
- `GET /dashboard` - Dashboard do usuário (redireciona conforme tipo)

## 🤝 Contribuindo

Este é um projeto educacional. Sinta-se livre para:
- Reportar bugs
- Sugerir melhorias
- Fazer fork e modificar

## 📄 Licença

Projeto desenvolvido para fins educacionais.

## 👨‍💻 Desenvolvido com

- ❤️ Paixão por código
- ☕ Muito café
- 🍕 Inspiração em delivery de comida

---

**DeliveryPro** - Sistema Profissional de Delivery 🚀
