<!-- 70646975-805b-4775-a391-71a2ddda6e10 c5bb5065-dbdb-426b-b942-a7b47921b8fe -->
# Complete Ikarus 3D ML Assignment (1-Hour Sprint)

## Critical Missing Components

### 1. Jupyter Notebooks (REQUIRED Deliverables)

**Create `notebooks/data_analysis.ipynb`:**

- Convert existing `scripts/data_analysis.py` to interactive notebook
- Add markdown cells with detailed comments explaining each analysis step
- Include visualizations: price distribution, category breakdown, brand analysis
- Document insights and findings

**Create `notebooks/model_training.ipynb`:**

- Load dataset and prepare features
- Train/load pre-trained models: sentence-transformers (NLP), ResNet50 (CV)
- Evaluate model performance with metrics (accuracy, precision, similarity scores)
- Document model selection reasoning and results
- Save embeddings for Pinecone

### 2. LangChain Integration (REQUIRED)

**Create `backend/services/langchain_service.py`:**

- Use LangChain with Azure OpenAI (user already has API key)
- Implement embedding chain for text vectorization
- Implement GenAI chain for product description generation
- Use `PromptTemplate` for creative descriptions

**Update recommendation flow to use LangChain:**

- Replace TF-IDF with LangChain embeddings
- Generate AI descriptions for recommended products

### 3. GenAI Product Descriptions (REQUIRED)

**Backend:** Add endpoint `/api/v1/products/{id}/generate-description`

- Use LangChain + Azure OpenAI GPT-4
- Generate creative descriptions based on product features

**Frontend:** Display AI-generated descriptions

- Show "AI Generated Description" section in product cards
- Add loading state while generating

### 4. Computer Vision (CV) - REQUIRED

**Implement in `backend/services/cv_service.py`:**

- Use pre-trained ResNet50 from torchvision
- Extract image features from product URLs
- Classify product categories from images
- Store image embeddings

### 5. NLP Product Grouping (REQUIRED)

**Implement in `backend/services/nlp_service.py`:**

- Use sentence-transformers for semantic similarity
- Group similar products by description/title embeddings
- Implement category clustering

### 6. Pinecone Vector Database (REQUIRED)

**Populate Pinecone with all 312 products:**

- Run setup script to create/populate index
- Store combined text + image embeddings
- Include metadata: title, brand, price, categories, image URL
- Update recommendation service to query Pinecone

**Integrate with API:**

- Use Pinecone for all product searches
- Return top-k similar products with scores

### 7. Analytics Backend Integration

**Create `backend/routers/analytics.py`:**

- Endpoint to return real analytics from dataset
- Category distribution, price stats, brand counts
- Connect frontend to real data instead of mock

## Implementation Priority (60 minutes)

**Minutes 0-15: Notebooks**

- Create `data_analysis.ipynb` with EDA and visualizations
- Create `model_training.ipynb` with model loading and evaluation

**Minutes 15-30: LangChain + GenAI**

- Implement `langchain_service.py` with Azure OpenAI
- Add description generation endpoint
- Update frontend to display AI descriptions

**Minutes 30-45: CV/NLP Services**

- Implement `cv_service.py` with ResNet50
- Implement `nlp_service.py` with sentence-transformers
- Create combined embeddings

**Minutes 45-55: Pinecone Population**

- Generate embeddings for all 312 products
- Populate Pinecone index
- Update recommendation service to use Pinecone

**Minutes 55-60: Final Integration & Testing**

- Connect analytics backend to frontend
- Test end-to-end flow
- Verify all requirements met

## Key Files to Create/Modify

**New Files:**

- `notebooks/data_analysis.ipynb`
- `notebooks/model_training.ipynb`
- `backend/services/langchain_service.py`
- `backend/services/cv_service.py`
- `backend/services/nlp_service.py`
- `backend/routers/analytics.py`
- `scripts/populate_pinecone.py`

**Modify:**

- `backend/services/recommendation_service.py` - Use Pinecone + LangChain
- `backend/main.py` - Add analytics router
- `frontend/src/pages/RecommendationPage.tsx` - Show AI descriptions
- `frontend/src/pages/AnalyticsPage.tsx` - Use real API data

## Success Criteria

All assignment requirements met:

- ✅ ML: Recommendation model using embeddings
- ✅ NLP: Text analysis and product grouping
- ✅ CV: Image classification with ResNet50
- ✅ GenAI: AI-generated product descriptions
- ✅ Vector DB: Pinecone storing 312 products
- ✅ LangChain: Used for GenAI and embeddings
- ✅ Frontend: React with recommendations + AI descriptions
- ✅ Analytics: Real data dashboard
- ✅ Notebooks: 2 .ipynb files with detailed comments

### To-dos

- [ ] Create data_analysis.ipynb and model_training.ipynb with detailed comments and evaluations
- [ ] Implement LangChain service with Azure OpenAI for embeddings and GenAI descriptions
- [ ] Create CV service (ResNet50) and NLP service (sentence-transformers) for image/text processing
- [ ] Generate embeddings and populate Pinecone with all 312 products
- [ ] Update recommendation service to use Pinecone, add GenAI endpoint, add analytics API
- [ ] Display AI-generated descriptions and connect analytics to real backend