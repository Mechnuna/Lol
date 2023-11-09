from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)

from recipes.models import Favorite, Tag, Shoppingcart, Ingredient, Recipe
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, MiniRecipesSerializer,
                          ShoppingcartSerializer, FavoriteSerializer)
from .services import shoppingcart


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminOrReadOnly]

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({"error": "уже в Избранном"},
                                status=HTTP_400_BAD_REQUEST)

            serializer = FavoriteSerializer(recipe, data=request.data,
                                            context={"request": request})
            serializer.is_valid()

            Favorite.objects.create(user=user, recipe=recipe)
            # fav_recipe = get_object_or_404(Recipe, id=pk)
            serializer = MiniRecipesSerializer(recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                Favorite.objects.filter(user=user, recipe=recipe).delete()
                return Response({"log": "Вы удалили рецепт из Избранного"},
                                status=HTTP_200_OK)
            return Response({"error": "not in Favorites"},
                            status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if Shoppingcart.objects.filter(user=user, recipe=recipe).exists():
                return Response({"error": "уже в Корзине"},
                                status=HTTP_400_BAD_REQUEST)

            serializer = ShoppingcartSerializer(recipe, data=request.data,
                                                context={"request": request})
            serializer.is_valid()

            Shoppingcart.objects.create(user=user, recipe=recipe)
            # shop_cart = get_object_or_404(Recipe, id=pk)
            serializer = ShoppingcartSerializer(recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if Shoppingcart.objects.filter(user=user, recipe=recipe).exists():
                Shoppingcart.objects.filter(user=user, recipe=recipe).delete()
                return Response({"log": "Вы удалили рецепт из Списка покупок"},
                                status=HTTP_200_OK)
            return Response({"error": "not in Shopping Cart"},
                            status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        shoping_cart = shoppingcart(request)
        response = HttpResponse(shoping_cart,
                                content_type="text.txt; charset=utf-8")
        filename = 'loaded_ingr.txt'
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
